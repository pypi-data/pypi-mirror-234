# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from Action import *


""" Add your callback function here """
## Rank operation definitions
# Rank Operation 1

import json
import openai
from multillm.MultiLLM import MultiLLM


def extract_rank_info(GPT_code_quality_score,  GPT_space_time_efficiency_score,GPT_code_quality_exp, 
    GPT_space_time_efficiency_exp,BARD_code_quality_score,
    BARD_space_time_efficiency_score,BARD_code_quality_exp,  
    BARD_space_time_efficiency_exp,LLAMA2_code_quality_score,
    LLAMA2_space_time_efficiency_score,LLAMA2_code_quality_exp,  
    LLAMA2_space_time_efficiency_exp):
    '''
    Prints basic "ranking" metrics and information

    Inputs:
        -GPT_code_quality_score (str): Code Quality Score out of 10 of GPT response
        -GPT_space_time_efficiency_score (str): space_time_efficiency Score out of 10 of GPT response
        -GPT_code_quality_exp (str): Code Quality short explanation of GPT response
        -GPT_space_time_efficiency_exp (str): space_time_efficiency short explanation of GPT response
        -BARD_code_quality_score (str): Code Quality Score out of 10 of BARD response
        -BARD_space_time_efficiency_score (str): space_time_efficiency Score out of 10 of BARD response
        -BARD_code_quality_exp (str): Code Quality short explanation of BARD response
        -BARD_space_time_efficiency_exp (str): space_time_efficiency short explanation of BARD response
        -LLAMA2_code_quality_score (str): Code Quality Score out of 10 of LLAMA2 response
        -LLAMA2_space_time_efficiency_score (str): space_time_efficiency Score out of 10 of LLAMA2 response
        -LLAMA2_code_quality_exp (str): Code Quality short explanation of LLAMA2 response
        -LLAMA2_space_time_efficiency_exp (str): space_time_efficiency short explanation of LLAMA2 response
      
    '''

    return GPT_code_quality_score,  GPT_space_time_efficiency_score,GPT_code_quality_exp,  GPT_space_time_efficiency_exp,BARD_code_quality_score, BARD_space_time_efficiency_score,BARD_code_quality_exp,  BARD_space_time_efficiency_exp,LLAMA2_code_quality_score, LLAMA2_space_time_efficiency_score,LLAMA2_code_quality_exp,  LLAMA2_space_time_efficiency_exp

def return_ranking_result(args_dict):
    # Loop through the scores and calculate the sum and count for each category
    bard_sum = 0
    bard_count = 0
    gpt_sum = 0
    gpt_count = 0
    llama2_count = 0
    llama2_sum = 0
    for key, value in args_dict.items():
        if key.startswith("BARD") and key.endswith("score"):
            bard_sum += float(value)
            bard_count += 1
        elif key.startswith("GPT") and key.endswith("score"):
            gpt_sum += float(value)
            gpt_count += 1
        elif key.startswith("LLAMA2") and key.endswith("score"):
            llama2_sum += float(value)
            llama2_count += 1
    # Calculate the average scores
    average_gpt_score = gpt_sum / gpt_count
    average_bard_score = bard_sum / bard_count
    average_llama2_score = llama2_sum / llama2_count
    args_dict["GPT_avg_score"] = average_gpt_score
    args_dict["BARD_avg_score"] = average_bard_score
    args_dict["LLAMA2_avg_score"] = average_llama2_score

    print("Average GPT score:", average_gpt_score)
    print("Average BARD score:", average_bard_score)
    print("Average LLAMA2 score:", average_llama2_score)
    return args_dict

my_custom_functions = [
    {
        'name': 'extract_rank_info',
        'description': 'Get scores out of 10 followed by short explanation for various metrics  from the GPT responses',
        'parameters': {
            'type': 'object',
            'properties': {
                'GPT_code_quality_score': {
                    'type': 'string',
                    'description': 'Code Quality Score out of 10 of GPT response'
                },
                'GPT_space_time_efficiency_score': {
                    'type': 'string',
                    'description': 'space_time_efficiency Score out of 10 of GPT response'
                },
                'GPT_code_quality_exp': {
                    'type': 'string',
                    'description': 'Code Quality explanation of  GPT response right after score in response'
                },
                'GPT_space_time_efficiency_exp': {
                    'type': 'string',
                    'description': 'space_time_efficiency explanation of GPT response right after score in response'
                },
                'BARD_code_quality_score': {
                    'type': 'string',
                    'description': 'Code Quality Score out of 10 of BARD response'
                },
                'BARD_space_time_efficiency_score': {
                    'type': 'string',
                    'description': 'space_time_efficiency Score out of 10 of BARD response'
                },
                'BARD_code_quality_exp': {
                    'type': 'string',
                    'description': 'Code Quality explanation of  BARD response right after score in response'
                },
                'BARD_space_time_efficiency_exp': {
                    'type': 'string',
                    'description': 'space_time_efficiency explanation of BARD response right after score in response'
                },
                'LLAMA2_code_quality_score': {
                    'type': 'string',
                    'description': 'Code Quality Score out of 10 of LLAMA2 response'
                },
                'LLAMA2_space_time_efficiency_score': {
                    'type': 'string',
                    'description': 'space_time_efficiency Score out of 10 of LLAMA2 response'
                },
                'LLAMA2_code_quality_exp': {
                    'type': 'string',
                    'description': 'Code Quality explanation of  LLAMA2 response right after score in response'
                },
                'LLAMA2_space_time_efficiency_exp': {
                    'type': 'string',
                    'description': 'space_time_efficiency explanation of LLAMA2 response right after score in response'
                }
            }
        }
    }
]

def transform_json(input_json):
    output_json = {}
    for key in input_json:
        # Split the key using '_' as a separator
        parts = key.split('_')

        # Extract the first part as the group name and the second part as the field name
        group_name = parts[0]
        field_name = '_'.join(parts[1:])

        # Create a dictionary for the group if it doesn't exist
        if group_name not in output_json:
            output_json[group_name] = {}

        # Add the field to the group dictionary with the corresponding value from the input JSON
        output_json[group_name][field_name] = input_json[key]
    return output_json


def rank_CB(responses, config=None):
    """ rank_CB is called by Rank() class, with the arguments dict and config
    Args:
        responses: dictionary of key,value in the form of {"llm-name" : "response"}
        config: name of config file used during the multillm calls..
    Description:
        The purpose of this callback is to rank the responses of the various LLMs from the responses dictionary,
        and to return the result as a text string or markdown.
        For example: if responses = {"GPT" : gpt-response , "BARD" : bard-response}
        this callback will parse, analyze and rank the responses from "GPT" and "BARD" and return a ranked result"
    """
    
    """ Read Config Fild data"""
    print("Responses are:\n\n")
    print(responses)
    conf_data = MultiLLM.read_config()
    if conf_data:
        """ Get the credentials for GPT LLM"""
        try:
            llms = conf_data["Config"]["MultiLLM"]["llms"]  
            for llm in llms:
                if llm['class_name'] == "GPT":
                    credentials = llm['credentials']
                    openai_auth_file = credentials
                    if not os.path.exists(openai_auth_file):
                        return ("(rank_CB) could not find GPT credentials: {0}" .format(openai_auth_file))
                    break
        except Exception as e:
            return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
    try:
        with open(openai_auth_file, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            try:
                openai.organization = data['organization']
                openai.api_key = data['api_key'] 
            except Exception as e:
                print('(LLM.check_key(): {0}' .format(str(e)))
                return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
    except Exception as e:
        print('(LLM.check_key(): {0}' .format(str(e)))
        return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))

          
    messages = [
            
            { "role": "system", "content":"Given the following LLMs and their responses,give each code a score out of 10 for following 2 metrics for the BARD key, GPT key and LLAMA2 key.Code quality,  and space time efficiency with a short explanation for each.Return these 6 scores for the responses, 2 scores for GPT ,2 scores for BARD and 2 scores for LLAMA2."}


    ]

    
    no_code_count = 0
    responses_count = len(responses.items())
  
    for llm,response in responses.items():
        #print('llm: {0} Response {1}' .format(llm, response))
        if not response or "returned no code" in response:
            no_code_count += 1
        messages.append({"role": "user", "content": f"{llm}: {response}"})

    if no_code_count == responses_count:
        return('Sorry, we can only rank code at the moment!')
    
    exit = False
    
    while not exit:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions = my_custom_functions,
            function_call = 'auto'

        )

   
        func_args = response["choices"][0]["message"]["function_call"]["arguments"]
        print(response["choices"][0]["message"])
        print(func_args)
    

        func_args_json = json.loads(func_args)
        if len(func_args_json) == 12:
            exit = True
        else:
            print("Rerunning LLM ranking")

    updated_func_args_json = return_ranking_result(func_args_json)
    updated_func_args_json = transform_json(updated_func_args_json)
    
    return updated_func_args_json


def rank_CB_no_code(responses, config=None):
    """ rank_CB is called by Rank() class, with the arguments dict and config
    Args:
        responses: dictionary of key,value in the form of {"llm-name" : "response"}
        config: name of config file used during the multillm calls..
    Description:
        The purpose of this callback is to rank the responses of the various LLMs from the responses dictionary,
        and to return the result as a text string or markdown.
        For example: if responses = {"GPT" : gpt-response , "BARD" : bard-response}
        this callback will parse, analyze and rank the responses from "GPT" and "BARD" and return a ranked result"
    """
    
    """ Read Config Fild data"""
    print("Responses are:\n\n")
    print(responses)
   
    conf_data = MultiLLM.read_config()
    if conf_data:
        """ Get the credentials for GPT LLM"""
        try:
            llms = conf_data["Config"]["MultiLLM"]["llms"]  
            for llm in llms:
                if llm['class_name'] == "GPT":
                    credentials = llm['credentials']
                    openai_auth_file = credentials
                    if not os.path.exists(openai_auth_file):
                        return ("(rank_CB) could not find GPT credentials: {0}" .format(openai_auth_file))
                    break
        except Exception as e:
            return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
    try:
        with open(openai_auth_file, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            try:
                openai.organization = data['organization']
                openai.api_key = data['api_key'] 
            except Exception as e:
                print('(LLM.check_key(): {0}' .format(str(e)))
                return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
    except Exception as e:
        print('(LLM.check_key(): {0}' .format(str(e)))
        return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))

          
    messages = [
            {"role": "system", "content":"Given the following LLMs and their responses in rank the BARD answer, GPT answer and LLAMA2 answer. . Respond only with the answer name and explanation in bullet points. Return the response in markdown format"}
            #{ "role": "system", "content":"You are an LLM tasked with ranking other LLMs, given the following LLMs and their responses, rank them. Response only with a name and explanation in a python list"}
    ]

    for llm,response in responses.items():       
        messages.append({"role": "user", "content": f"{llm}: {response}"})
    
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
