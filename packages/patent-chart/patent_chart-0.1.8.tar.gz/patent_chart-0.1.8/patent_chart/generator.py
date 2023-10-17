import os
import re
import time

import openai
import tiktoken
from dotenv import load_dotenv

from . import parser

load_dotenv()

model_name_to_token_limit = {
    'gpt-4': 8192,
    'gpt-3.5-turbo-16k': 16384,
    'gpt-3.5-turbo': 4096,
    'gpt-3.5-turbo-16k-0613': 16384,
}

def num_tokens_in_text(text, model="gpt-3.5-turbo-0613"):
  """Returns the number of tokens in a string."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  return len(encoding.encode(text))

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def prepare_prior_art_source():
    pass

def prepare_patent():
    pass

# concatenate completions and renumber
# TODO: make 3 a parameter
def concatenate_completions_for_reranking(completions):
    concatenated_completions = ''
    for i, completion in enumerate(completions):
        completion_content = completion['choices'][0]['message']['content']
        completion_content1, completion_content = completion_content.split('\n2.')
        completion_content1 = completion_content1.lstrip('1. ')
        completion_content2, completion_content = completion_content.split('\n3.')
        completion_content3 = completion_content
        
        concatenated_completions += f'{int_to_roman(i*3 + 1)}. {completion_content1}\n'
        concatenated_completions += f'{int_to_roman(i*3 + 2)}. {completion_content2}\n'
        concatenated_completions += f'{int_to_roman(i*3 + 3)}. {completion_content3}\n'
    return concatenated_completions, 3 * len(completions)

# Reranking utility functions
def int_to_roman(n: int) -> str:
    if not (0 < n < 4000):
        raise ValueError("Input integer must be between 1 and 3999")
    
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    
    for i in range(len(ints)):
        count = int(n / ints[i])
        result.append(nums[i] * count)
        n -= ints[i] * count
    
    return ''.join(result)

# parse reranked completions
def parse_reranked_completions(reranked_completion, n_completions):
    # First lstrip prelude before 1.
    # Find index of '1. ' and slice
    reranked_completion = reranked_completion[reranked_completion.index('1. '):]
    
    # Split on i. for i in range(1, n_completions + 1)
    # Then lstrip roman numeral and period
    roman_numeral_regex_pattern = r''
    for i in range(1, n_completions + 1):
        roman_numeral_regex_pattern += f'{int_to_roman(i)}\. '
        if i < n_completions:
            roman_numeral_regex_pattern += '|'
    roman_numeral_regex = re.compile(roman_numeral_regex_pattern)
    
    parsed_completions = []
    for i in range(1, n_completions + 1):
        if i == n_completions:
            parsed_completion = reranked_completion
        else:
            parsed_completion, reranked_completion = reranked_completion.split(f'{i+1}. ', maxsplit=1)
        if i == 1:
            parsed_completion = parsed_completion.lstrip('1. ')
        parsed_completion = re.sub(roman_numeral_regex, '', parsed_completion)
        parsed_completion = parsed_completion.lstrip(' "')
        parsed_completion = parsed_completion.rstrip(' \n"')
        parsed_completions.append(parsed_completion)
        
    return parsed_completions


def openai_prompt_select_passages_from_prior_art_portion(all_but_claims, claims, claim_element, prior_art_passage):
    # TODO: make 3 a parameter
    messages = [
        {"role": "system", "content": "You are an associate at a big law firm. Your task is to read the written description and of an invention disclosed in a patent and the full set of claims in the patent and interpret a single claim element that I select from the claims of the patent in light of the written description and the full set of claims. Then I'm going to give you a passage from of prior art and you need to pick three distinct sub-passages from the passage that you believe are the most semantically similar to the claim element interpreted in light of the written description and the full set of claims. Please output only those three passages, each preceded only by the numberings 1., 2., and 3. and a space."},
        {"role": "user", "content": f"Written description of invention: {all_but_claims}"},
        {"role": "user", "content": f"Full set of claims: {claims}"},
        {"role": "user", "content": f"Selected claim element: {claim_element}"},
        {"role": "user", "content": f"Prior art passage: {prior_art_passage}"},
    ]
    return messages

def openai_prompt_rank_selected_passages(all_but_claims, claims, claim_element, chosen_prior_art_passage, n_completions):
    messages = [
        {"role": "system", "content": f"Your task is to read the written description and of an invention disclosed in a patent and the full set of claims in the patent and interpret a single claim element that I select from the claims of the patent in light of the written description and the full set of claims. Then I'm going to give you {n_completions} sub-passages from the prior art passage i presented to you that you chose because they were the most semantically similar to the selected claim element interpreted in light of the written description and the full set of claims. Please rank these {n_completions} passages in descending order of similarity to the selected claim element interpreted in light of the written description and the full set of claims."},
        {"role": "user", "content": f"Written description of invention: {all_but_claims}"},
        {"role": "user", "content": f"Claim element: {claim_element}"},
        {"role": "user", "content": f"Prior art passages to rank: {chosen_prior_art_passage}"},
    ]
    return messages


# def openai_chat_completion_request_with_retry(model_name, messages, backoff_factor=2, backoff_override=None):
#     """Send a chat completion request to OpenAI with retries."""
#     # Up to 7 to get around per limit rate limits
#     for i in range(1, 7):
#         try:
#             completion = openai.ChatCompletion.create(
#                 model=model_name,
#                 messages=messages
#             )
#             return completion
#         except openai.error.OpenAIError as e:
#             if backoff_override is not None:
#                 time.sleep(backoff_override)
#             else:
#                 time.sleep(backoff_factor**i)
#             print(e)
#             continue
#         except Exception as e:
#             raise e
#     raise Exception("Failed to send chat completion request to OpenAI after 4 retries.")

# def generate_passages(
#         patent_text: list[str], 
#         patent_claims: parser.Claims | str, 
#         prior_art_text: list[str], 
#         claim_element_text: str, 
#         model_name: str='gpt-4'):
    
#     patent_parser = parser.PatentParser.from_pages(patent_text)
#     patent_all_but_claims = patent_parser.parse_all_but_claims()
#     if isinstance(patent_claims, parser.Claims):
#         patent_claims = '\n'.join([parser.serialize_claim(c) for c in patent_claims.claims])

#     # Find maximum size prior art split that fits within OpenAI's token limit
#     token_limit = model_name_to_token_limit[model_name]

#     # Cut off claims portion of prior art if it's a patent
#     # claims_start = parser.find_claims_start_from_pages(prior_art_text)
#     # if claims_start is not None:
#     #     claims_start_page = prior_art_text[claims_start.page_index]
#     #     prior_art_text = prior_art_text[:claims_start.page_index]
#     #     prior_art_text.append(claims_start_page[:claims_start.start_index])
#     # XXX: hardcoded to only work with krishna. TODO: parse prior art patent source to make it better digestible to LLM
#     prior_art_text = prior_art_text[12:22]
#     prior_art_text = '\n'.join(prior_art_text)

#     # XXX: hardcoded to only work with 448 patent.
#     patent_all_but_claims = \
#         """
#         US 7,069,448 B2 
#         1. 
#         CONTEXT ORIENTED CRYPTO 
#         PROCESSING ON A PARALLEL 
#         PROCESSOR ARRAY 
#         CROSS-REFERENCE TO RELATED 
#         APPLICATIONS 
#         This disclosure claims the priority benefit of, and incor porates by reference in its entirety, U.S. provisional patent 
#         application Ser. No. 60/337,530, filed on Dec. 5, 2001. Additionally, this disclosure is related to the following co-pending U.S. patent applications: U.S. patent application 
#         Ser. No. 09/023,672, entitled “Cryptographic Key Split 
#         Combiner.” filed on Feb. 13, 1998 by SCHEIDT et al.; Ser. No. 09/874.364, entitled “Cryptographic Key Split Com 
#         biner.” filed on Jun. 6, 2001 by SCHEIDT et al.: Ser. No. 09/917,795, entitled “Cryptographic Key Split Combiner.” 
#         filed on Jul. 31, 2001 by SCHEIDT et al.; Ser. No. 09/917, 794, entitled “Cryptographic Key Split Combiner, filed on 
#         Jul. 31, 2001 by SCHEIDT et al.; Ser. No. 09/917,802, entitled “Cryptographic Key Split Combiner, filed on Jul. 
#         31, 2001 by SCHEIDT et al.; Ser. No. 09/917,807, entitled “Cryptographic Key Split Combiner, filed on Jul. 31, 2001 
#         by SCHEIDT et al.; Ser. No. 09/992,529, entitled “Crypto graphic Key Split Combiner.” filed on Nov. 20, 2001 by 
#         SHEIDT et al.: Ser. No. 10/147.433, entitled “Cryptographic Key Split Binding Process and Apparatus.” filed on May 16, 
#         2002 by SCHEIDT et al.; Ser. No. 09/205,221, entitled 
#         “Access Control and Authorization System, filed on Dec. 4, 
#         1998 by SCHEIDT et al.; and Ser. No. 10/278,765, entitled 
#         "Access Control and Authorization,' filed on Oct. 22, 2002 
#         by SCHEIDT et al. 
#         FIELD OF THE INVENTION 
#         The present invention relates to cryptographic processing, parallel processing, and parallel cryptographic processing. 
#         More specifically, the present invention relates to context oriented cryptographic processing in a parallel processing 
#         environment. 
#         BACKGROUND OF THE INVENTION 
#         Cryptography has been used as a means to protect elec 
#         tronic information from unauthorized alteration, manipula 
#         tion and access. From Internet transactions to mobile tele 
#         phone communications to database management, the frequency and importance of data storage and communica tion have grown exponentially in recent years. 
#         As the importance of data storage and communications have grown, computer security has become equally impor 
#         tant to safe guard sensitive data and to limit access to 
#         computer resources to authorized individuals. With the increased importance of computer security, security-based 
#         measures have also grown in complexity and strength. Due 
#         to increased complexities, the costs associated with effec tuating cryptographic schemes have also grown. In particu 
#         lar, processing resources can be adversely affected when complex cryptographic schemes are employed. 
#         Further, as larger amounts of electronic information are cryptographically secured, processing resources can also be 
#         adversely affected when cryptographic schemes are 
#         employed, and can be further adversely affected when the cryptographic schemes are complex. 
#         Cryptographic schemes have been applied to parallel 
#         processing environments to increase necessary processing 
#         resources, as well as to provide processing efficiency. However, there remains a need for an efficient manner of effec tuating cryptographic processing in a parallel processing 
#         environment. There additionally remains a need for a con text-oriented manner of facilitating cryptographic process 
#         ing in a parallel processing environment. 
#         BRIEF SUMMARY OF THE INVENTION 
#         The present invention provides cryptographic processing 
#         of input data in a parallel processing environment, and can be employed in myriad applications. For example, the 
#         present invention can be applied to telecommunications cryptographic processing on trunk lines. Further, the present invention can provide fine granularity cryptographic sepa 
#         ration between virtual circuits in a trunk. Also, the present invention can be applied to Asynchronous Transfer Mode 
#         (ATM) virtual circuits (“VCs'), hierarchical framing structures in a Synchronous Optical Network (“SONET), 
#         and transaction threads to a database. 
#         In an exemplary embodiment, the present invention can be embodied in a system for cryptographic processing of 
#         input data on a parallel processor array that includes a 
#         plurality of processors, and includes: a format filter, a 
#         control unit, a first distributor, and a second distributor. The 
#         format filter extracts control data and main data from the 
#         input data, while the control unit receives the control data 
#         from the format filter, and forwards, based at least in part on the control data, at least one respective control parameter and at least one respective cryptographic parameter to each 
#         of the plurality of processors. The first distributor, such as a 
#         Switching matrix, for example, receives the main data from 
#         the format filter, and distributes to each of the plurality of processors a respective at least a portion of the main data. 
#         The second Switching matrix, such as a Switching matrix, for example, receives respective output information from each 
#         of the plurality of processors, and generates, based at least 
#         in part on the respective output information, output data. Each processor generates its respective output information 
#         based at least in part on its at least one respective control parameter and its at least one respective cryptographic 
#         parameter. The output data can be a cryptographic process 
#         ing result. The following are exemplary aspects of the present inven 
#         tion: 
#         The control unit can be further adapted to provide state data that represents a particular state of the processor array. 
#         The main data can be encrypted data, while the output data 
#         can be unencrypted data. Likewise, the main data can be unencrypted data, while the output data can be encrypted 
#         data. 
#         Further, each respective at least a portion of the main data 
#         can be a multiplexed process stream. Moreover, each of the 
#         plurality of processors can initialize based at least in part on 
#         the at least one respective control parameter received from 
#         the control unit. Also, each of the plurality of processors can perform a cryptographic function based at least in part on the at least one respective cryptographic parameter received 
#         from the control unit. 
#         Additionally, the at least one respective cryptographic 
#         parameter can be keying data. And further, at least one of the 
#         first distributor and the second distributor can be a switching 
#         matrix. 
#         In another exemplary embodiment, the present invention can be embodied in a method of cryptographically process ing input data in a system comprising a parallel processor array having a plurality of processors. Accordingly, the 
#         method can include acts of extracting, from the input data, US 7,069,448 B2 
#         3 
#         control data and main data; forwarding, based at least in part on the control data, at least one respective control parameter and at least one respective cryptographic parameter to each 
#         of the plurality of processors; distributing to each of the plurality of processors a respective at least a portion of the 
#         main data; generating, by each of the plurality of processors, 
#         respective output information based at least in part on the at 
#         least one respective control parameter and the at least one respective cryptographic parameter; and generating output 
#         databased at least in part on the respective output informa tion. The output data can be a cryptographic processing 
#         result. 
#         The following are further exemplary aspects of the 
#         present invention: 
#         The method can further include providing state data representative of a state of the processor array. The main 
#         data can be encrypted data, while the output data can be 
#         unencrypted data. Likewise, the main data can be unen crypted data, while the output data can be encrypted data. 
#         Further, each respective at least a portion of the main data can be a multiplexed process stream. 
#         The method can further include initializing, by each of the plurality of processors, based at least in part on the at least 
#         one respective control parameter. The method can further include performing, by each of the plurality of processors, a 
#         cryptographic function based at least in part on the at least one respective cryptographic parameter. Additionally, the at 
#         least one respective cryptographic parameter can be keying 
#         data. 
#         BRIEF DESCRIPTION OF THE DRAWINGS 
#         The present invention is illustrated by way of example 
#         and not in limitation in the figures of the accompanying drawings, in which: 
#         FIG. 1 illustrates an exemplary embodiment of the present 
#         invention, in which a system includes a format filter, a 
#         control unit, a Switching matrix, and an inverse matrix. FIG. 2 illustrates another exemplary embodiment of the 
#         present invention, in which a system includes a format filter, 
#         a control unit, a first distributor, and a second distributor. FIG. 3 illustrates an exemplary method according to 
#         another exemplary embodiment of the present invention. 
#         DETAILED DESCRIPTION OF THE 
#         INVENTION 
#         Initial reference is made to FIG. 1, which illustrates a system according to an exemplary embodiment of the 
#         present invention. As shown in FIG. 1, a system for cryp tographic processing of input data 101 on a parallel proces 
#         sor array that includes a plurality of processors 102, can 
#         include the following: a format filter 110, a control unit 120, 
#         a first distributor 130, and a second distributor 140. Illus tratively, input data 101 can be based on any of a plurality 
#         of data structures, such as, for example, an ATM cell 
#         structure, hierarchical framing structure in SONET, or trans 
#         action threads for a database. 
#         Format filter 110 can be adapted to extract control data 
#         111 and main data 112 from input data 101. Thus, control data 111 is contained within input data 101, and can be 
#         formatted within a header structure thereof, for example. Control data 111 is used for encryption or decryption, which 
#         is further described below. 
#         Where main data 112 is unencrypted data, control data 111 
#         is utilized in the encryption of main data. Thus, control data 
#         111 can be used to drive control and cryptographic functions for the encryption of main data 112. For example, here, 
#         control data 111 can include framing information relevant to 
#         bundled sub-threads or virtual circuits and sessions in an 
#         input stream. 
#         Where main data 112 is encrypted data, control data 111 is utilized in the decryption of main data. Accordingly, 
#         control data 111 can be used to drive the control and 
#         cryptographic functions of the system. For example, here, 
#         control data 111 can include at least one cryptographic 
#         credential. A cryptographic credential defines one or more 
#         access levels. Thus, through the inclusion of at least one 
#         credential contained in control data 111, the control data can be used for encryption or decryption within the system. 
#         For example, as described in U.S. patent application Ser. 
#         No. 09/205,221, entitled "Access Control and Authorization System,” filed on Dec. 4, 1998 by SCHEIDT et al., a cryptographic credential can include a user's or entity's assigned permissions to labels and algorithms (such as, for example, one or more key splits, passwords, seed data 
#         instances, or other cryptographic parameters). As a further example, a credential can be encrypted, with a system password, for example, to improve security. 
#         As further shown in FIG. 1, control unit 120 provides the parallel cryptographic processing initialization of processors 
#         102 based on control data 111, which is received from 
#         format filter 110. For example, initialization can be for various modes of cryptographic functionality, algorithms, key management parameters, and matrix configuration. 
#         Thus, based at least in part on control data 111, control unit 120 provides at least one respective control parameter 121 
#         and at least one respective cryptographic parameter 122 to 
#         each of the plurality of processors 102, which allows the 
#         initialization. Further, control unit 120 can additionally provide state data 123 that represents a particular state of the system at a particular point in time. 
#         First distributor 130 receives main data 112 from format 
#         filter 110, and distributes a respective at least a portion of 
#         main data 112 to each of the processors 102. Thus, each of the processors 102 is provided respective data upon which to perform a portion of the cryptographic workload relating to 
#         the particular cryptographic function employed. Upon respective cryptographic processing, each of processors 102 
#         provide output information 103 to second distributor 140. 
#         As also shown in FIG. 1, second distributor 140 receives respective output information 103 from processors 102, and 
#         based at least in part thereon, generates output data 104. which is the result of the parallel cryptographic processing. 
#         Thus, first and second distributors 130, 140 multiplex main data 112 into streams or threads according to the particular parallel processing scheme employed. Further, for example, 
#         first and second distributors 130, 140 can operate in a pair-wise mode to preserve the integrity of input data 101. 
#         Reference is now made to FIGS. 1 and 2. FIG. 2 illustrates 
#         additional exemplary aspects of the present invention. As 
#         shown in FIG. 2, first distributor (shown in FIG. 1) can be a switching matrix 230, for example; and second distributor 
#         140 can be switching matrix (inv) or inverse Switching 
#         matrix 240. As shown in FIG. 2, the system can further include a cryptographic key generator 222 that generates the 
#         at least one respective cryptographic parameter 122 based at 
#         least in part on control data 111, and provides the generated at least one respective cryptographic parameter to each of processors 202. For example, a generated parameter may be 
#         keying data. 
#         Key-based cryptographic schemes include some manner 
#         of generating keys, where such a manner can range from simple or arbitrary to complex, in whole or in part. For US 7,069,448 B2 
#         5 
#         example, key generation in asymmetric schemes can be relatively complex, as key pairs can be required to relate to 
#         each other according to complex mathematics. 
#         Also, for example, as described in U.S. patent application 
#         Ser. No. 09/023,672, entitled “Cryptographic Key Split 
#         Combiner, a key generator can include plural key split generators, which generate respective key splits based on 
#         seed data, by, for example, mathematically binding or ran domizing together plural key splits to provide a key. Or, a 
#         key split generator can simply include a randomizer and/or a binder for randomizing and/or binding together key splits. 
#         For example, a random split generator can generate a 
#         random key split based on reference data. The random split generator can generate a random or pseudo-random 
#         sequence based on reference data, chronological data, or 
#         reference and static data, which may be updated. For example, updating static data can be by modifying a prime 
#         number divisor of the static data. Other key split generators can include, for example, a token split generator for gener 
#         ating a token key split based on label data and/or organiza 
#         tion data and/or static data; a console split generator for generating a console key split based on maintenance data, 
#         whether previous or current, and/or on static data; a bio metric split generator for generating a biometric key split 
#         based on biometric data, which can include biometric data 
#         vectors and on biometric combiner data, and/or static data. Label data may be read from a storage medium, and may 
#         include user authorization data. A location key split genera tor can generated a location key split based on real or virtual 
#         location data, such as for example, Global Position Satellite 
#         (“GPS) data, an Internet Protocol address. The resulting cryptographic key may be, for example, a stream of sym 
#         bols, at least one symbol block, or a key matrix. 
#         FIG. 3 illustrates an exemplary method, according to 
#         another exemplary embodiment of the present invention, of cryptographically processing input data in a system com prising a parallel processor array having a plurality of 
#         processors. As shown in FIG. 3. Such a method can include the following acts: extracting, from the input data, control 
#         data and main data (310); forwarding, based at least in part 
#         on the control data, at least one respective control parameter and at least one respective cryptographic parameter to each 
#         of the plurality of processors (320); distributing to each of the plurality of processors a respective at least a portion of 
#         the main data (330); generating, by each of the plurality of processors, respective output information based at least in 
#         part on the at least one respective control parameter and the at least one respective cryptographic parameter (340); and 
#         generating output databased at least in part on the respective 
#         output information (350), where the output data is a cryp tographic processing result. 
#         In another exemplary aspect of the invention, the method 
#         can further include an act of providing state data represen tative of a state of the processor array. 
#         In a further exemplary aspect of the invention, the main 
#         data can be encrypted data, while the output data can be decrypted data. Alternatively, the main data can be unen 
#         crypted data and the output data can be encrypted data. In 
#         still yet another exemplary aspect of the invention, each 
#         respective at least a portion of the main data can be a multiplexed process stream. 
#         In another exemplary aspect of the invention, the method 
#         can further include an act of initializing, by each of the plurality of processors, based at least in part on the at least one respective control parameter. Alternatively, or in addi 
#         tion, the method can further include an act of performing, by each of the plurality of processors, a cryptographic function 
#         based at least in part on the at least one respective crypto graphic parameter. 
#         In still yet another exemplary aspect of the invention, the at least one respective cryptographic parameter can be 
#         keying data. 
#         Referring again to FIGS. 1 and 2, in still yet a further 
#         exemplary aspect of the invention, a control parameter 121 
#         can determine which one or more processors of the proces sors 102 is to be used in a particular cryptographic routine. 
#         Thus, selective utilization of particular processors can extend system security. Additionally, input data 101 can 
#         further include application data, which identifies the identity 
#         or class of application associated with main data 112. Accordingly, selective utilization of processors can associ 
#         ated with the identity or class of application for which the 
#         cryptographic routine is needed. 
#         In the foregoing specification, the invention has been 
#         described with reference to specific embodiments thereof. It 
#         will, however, be evident that various modifications and/or changes may be made thereto without departing from the 
#         broader spirit and scope of the invention. Accordingly, the specification and drawings are to be regarded in an illustra 
#         tive and enabling, rather than a restrictive, sense. 
#         """

#     prior_art_split_count = 1
#     n_tokens_in_text = num_tokens_in_text(prior_art_text)
#     prior_art_splits = []
#     while True:
#         # Check all splits
#         candidate_splits = []
#         for i in range(prior_art_split_count):
#             if i == 0:
#                 candidate_split = prior_art_text[:len(prior_art_text) // prior_art_split_count]
#             else:
#                 candidate_split = prior_art_text[len(prior_art_text) // prior_art_split_count * i:len(prior_art_text) // prior_art_split_count * (i+1)]
#             candidate_splits.append(candidate_split)
#         num_tokens = [num_tokens_from_messages(
#             openai_prompt_select_passages_from_prior_art_portion(patent_all_but_claims, patent_claims, claim_element_text, split)
#         ) for split in candidate_splits]
#         if all([n <= token_limit - 0.05 * token_limit for n in num_tokens]):
#             prior_art_splits = candidate_splits
#             break
#         prior_art_split_count += 1

#     # Generate completions for each prior art split
#     completions = []
#     # XXX: remove hardcoded :2
#     for i, prior_art_split in enumerate(prior_art_splits[:2]):
#         messages = openai_prompt_select_passages_from_prior_art_portion(patent_all_but_claims, patent_claims, claim_element_text, prior_art_split)
#         # print num tokens in messages
#         print(num_tokens_from_messages(messages))
#         completion = openai_chat_completion_request_with_retry(model_name, messages)
#         print(completion)
#         completions.append(completion)

#     # Rerank completions
#     concatenated_completions, n_completions = concatenate_completions_for_reranking(completions)
#     print(concatenated_completions)
#     messages = openai_prompt_rank_selected_passages(patent_all_but_claims, patent_claims, claim_element_text, concatenated_completions, n_completions)
#     reranked_completion = openai_chat_completion_request_with_retry(model_name, messages)
#     print(reranked_completion)
#     reranked_completions = parse_reranked_completions(reranked_completion['choices'][0]['message']['content'], n_completions)

#     return reranked_completions


def generate_passages():
    pass