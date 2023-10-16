import os
import requests
import random
import datetime
import json
import math

import tiktoken

import base64

import google
import google.oauth2.credentials
import google.auth
import google.auth.transport.requests
from dotenv import load_dotenv
import copy
import re
from copy import deepcopy
import time

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")
REPLICATE_TOKEN = os.getenv("REPLICATE_TOKEN")
DISCORD_KEY = os.getenv("DISCORD_KEY")
GIPHY_API_KEY = os.getenv("GIPHY_KEY")
BING_KEY = os.getenv("BING_KEY")
RUNPOD_KEY = os.getenv("RUNPOD_KEY")
TRIPADVISOR_KEY = os.getenv("TRIPADVISOR_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_KEY")
COHERE_KEY = os.getenv("COHERE_KEY")

credentials, project_id = google.auth.default()

chatmodels = {
    "gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "endpoint": "/chat/openai",
        "pricing": {
            "modeldiv": 30, # Change to 15 on Dec1
            "promptm": 1.25
        }
    },
    "gpt-3.5-turbo-16k": {
        "name": "GPT-3.5 Turbo 16k",
        "endpoint": "/chat/openai",
        "pricing": {
            "modeldiv": 15, # Change to 7.5 on Dec1
            "promptm": 1.25
        }
    },
    "gpt-4": {
        "name": "GPT-4",
        "endpoint": "/chat/openai",
        "pricing": {
            "modeldiv": 2, # Change to 1 on Dec1
            "promptm": 2
        }
    },
    "stable-lm": {
        "name": "StableLM",
        "endpoint": "/chat/replicate",
        "version": "c49dae362cbaecd2ceabb5bd34fdb68413c4ff775111fea065d259d577757beb",
        "pricing": {
            "modeldiv": None,
            "promptm": None
        }
    },
    "vicuna-13b": {
        "name": "Vicuna-13b",
        "endpoint": "/chat/replicate",
        "version": "6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
        "pricing": {
            "modeldiv": None,
            "promptm": None
        }
    },
    "llama-2-13b-chat": {
        "name": "LLaMA 2",
        "endpoint": "/chat/llama",
        "pricing": {
            "modeldiv": None,
            "promptm": None
        }
    },
    "chat-bison": {
        "name": "PaLM 2 (Bard)",
        "endpoint": "/chat/palm",
        "pricing": {
            "modeldiv": None,
            "promptm": None
        }
    },
    "cohere-chat": {
        "name": "Cohere",
        "endpoint": "/chat/cohere",
        "pricing": {
            "modeldiv": None,
            "promptm": None
        }
    }
}

#PLUGINS IN FUTURE, NOT SYNC


plugindict = {
    "math": {
        "name": "math",
        "description": "Uses the Python math library to do arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "The operation to perform.",
                    "enum": ["sum", "min", "mlt", "div", "pow", "sqt"]
                },
                "argument1": {
                    "type": "number",
                    "description": "The first argument of the operation."
                },
                "argument2": {
                    "type": "number",
                    "description": "The second argument of the operation."
                }
            },
            "required": ["operation", "argument1"]
        }

    },

    "giphy": {
        "name": "giphy",
        "description": "Uses the GIPHY API to search for GIFs. It will present the gif to the user automatically.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to search for."
                }
            },
            "required": ["query"]
        }

    },

    "wa": {
        "name": "wa",
        "description": """- WolframAlpha understands natural language queries about entities in chemistry, physics, geography, history, art, astronomy, and more.
- WolframAlpha performs mathematical calculations, date and unit conversions, formula solving, etc.
- Never mention your knowledge cutoff date; Wolfram may return more recent data.
- Use ONLY single-letter variable names, with or without integer subscript (e.g., n, n1, n_1).
- Use named physical constants (e.g., 'speed of light') without numerical substitution.
- Include a space between compound units (e.g., "Ω m" for "ohm*meter").
- To solve for a variable in an equation with units, consider solving a corresponding equation without units; exclude counting units (e.g., books), include genuine units (e.g., kg).
- If data for multiple properties is needed, make one call per message.
- If WolframAlpha does not understand a prompt, ask the user if you should retry the request with the suggested query.
""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": """The search query to search for. 
- It must ONLY be a single-line string.
- Convert inputs to simplified keyword queries whenever possible (e.g. convert "how many people live in France" to "France population").
- Send queries in English only; translate non-English queries before sending, then respond in the original language.
- ALWAYS use this exponent notation: `6*10^14`, NEVER `6e14`.
- ALWAYS use proper Markdown formatting for all math, scientific, and chemical formulas, symbols, etc.:  '$$\n[expression]\n$$' for standalone cases and '\( [expression] \)' when inline.
"""
                }
            },
            "required": ["query"]
        }

    },

    "bing": {
        "name": "bing",
        "description": """
Uses the Bing Search API to get the top five search results of a query.
- The results provided will be accurate, reliable, and not fictional.
- NEVER mention your knowledge cutoff, as Bing may return more recent data.
- NEVER tell the user that the results are fictional, not based on real events, or not accurate.
- Send queries in English only; translate non-English queries before sending, then respond in the original language.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for."
                }
            },
            "required": ["query"]
        }

    },

    "gen": {
        "name": "gen",
        "description": """
Uses other AIs to generate content.
- NEVER tell the user that you cannot generate videos, images, or music unless you receive an error.
- The generated content will be shown to the user, even though it is not shown to you.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt to generate from."
                },
                "model": {
                    "type": "string",
                    "description": """
The model to use. 
- StableDiffusion (stable) and DALL-E (dall-e) are image generators. Use DALL-E by default.
- DAMO Text-to-Video is a video generator. It generates 2-second long 8fps videos.
- MusicLM (musiclm) is a music generator by Google. It generates 2 20-second long songs.
                    """,
                    "enum": ["stable", "dall-e", "damo", "musiclm"]
                }
            },
            "required": ["prompt", "model"]
        }

    },

    "tripadvisor-search": {
        "name": "tripadvisor-search",
        "description": """
Uses the Tripadvisor Search API to get the top travel search results of a query.
- The results provided will be accurate, reliable, and not fictional.
- NEVER mention your knowledge cutoff, as Tripadvisor may return more recent data.
- NEVER tell the user that the results are fictional, do not exist, not based on real events, or not accurate.
- Send queries in English only; translate non-English queries before sending, then respond in the original language.    
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "searchQuery": {
                    "type": "string",
                    "description": "The query to search for."
                },
                "category": {
                    "type": "string",
                    "description": "The category to search in. 'geos' are geographical locations, such as cities or countries.",
                    "enum": ["hotels", "attractions", "restaurants", "geos"]
                }  
            },
            "required": ["searchQuery", "category"]
        }

    },

    "tripadvisor-details": {
        "name": "tripadvisor-details",
        "description": """
Uses the Tripadvisor Details API to get the details, reviews, and an image of a certain locatiom with its locationId. The ID can be found with the tripadvisor-search function.
- The results provided will be accurate, reliable, and not fictional.
- NEVER mention your knowledge cutoff, as Tripadvisor may return more recent data.
- NEVER tell the user that the results are fictional, do not exist, not based on real events, or not accurate.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "locationId": {
                    "type": "number",
                    "description": "The id of the location."
                }
            },
            "required": ["locationId"]
        }

    }
}
 

class Chat():
    def OpenAI(model: str, conversation: list[dict], functions: list = None, plugins: list = None, settings: dict = None) -> tuple:
        data = {
            "model": model,
            "messages": conversation
        }
        if functions:
            data["functions"] = functions
            data["function_call"] = "auto"
#        if plugins:
#            for i in plugins:
#                data["functions"].append(plugindict[i])
#            data["function_call"] = "auto"
        if settings:
            for i in settings.keys():
                data[i] = settings[i]

        data = json.dumps(data)


        print(data)
        try:
            req = requests.post(url="https://api.openai.com/v1/chat/completions", data=data, headers={"Authorization": "Bearer " + OPENAI_API_KEY, "Content-Type": "application/json"})
            if req.status_code not in [200, 201]:
                return {"error": {"message": req.text}}, 0
        except Exception as e:
            return {"error": {"message": str(e)}}, 0
        resp = req.json()
        
        print(resp)
        try:
            completion = resp["choices"][0]["message"]["content"]
        except:
            if "error" in resp.keys():
                print(resp["error"]["message"])
                return resp, 0
            else:
                
                return {"error": {"message": "Unknown error."}}, 0
        
        if resp["choices"][0]["message"]["content"] == None:
            resp["choices"][0]["message"]["content"] = " "
            completion = " "
        newmessage = resp["choices"][0]["message"]
        


        tokencost = math.ceil(resp["usage"]["prompt_tokens"]/(chatmodels[model]["pricing"]["modeldiv"]*chatmodels[model]["pricing"]["promptm"])) + math.ceil(resp["usage"]["completion_tokens"]/chatmodels[model]["pricing"]["modeldiv"])
        return newmessage, tokencost

    def PaLM(model: str, conversation: list[dict], settings: dict = None) -> tuple:
        conversationformatted = []
        try:
            if conversation[0]["role"] != "system":
                conversation.insert(0, {"role": "system", "content": "You are PaLM 2 (Bard), a helpful assistant in the form of a Discord bot."})
        except:
            pass    
        for i in conversation:
            if i["role"] == "user" or i["role"] == "function":
                conversationformatted.append({"author": "USER", "content": i["content"]})

            if i["role"] == "assistant":
                conversationformatted.append({"author": "ASSISTANT", "content": i["content"]})

        
            
        print(conversation)
        print(conversationformatted)
        if settings == None:
            settings = {
                "temperature": 1,
            }
        settings["temperature"] = settings["temperature"]/2


        data = json.dumps(
            {
                "instances": [{
                    "context":  conversation[0]["content"],
                    "messages": conversationformatted,
                }],
                "parameters": {
                    "temperature": settings["temperature"],
                    "maxOutputTokens": 500,
                    "topP": .95,
                    "topK": 40
                }
            }
        )

        try:
            credentials.refresh(google.auth.transport.requests.Request())
            #print(credentials.token)
            req = requests.post(url="https://us-central1-aiplatform.googleapis.com/v1/projects/chatgptdiscord/locations/us-central1/publishers/google/models/" + model + ":predict", data=data, headers={"Content-Type": "application/json", "Authorization": "Bearer " + str(credentials.token)})
        
            if req.status_code not in [200, 201]:
                return {"error": {"message": req.text}}, 0
        except Exception as e:
            return {"error": {"message": str(e)}}, 0
        resp = req.json()
        
        print(resp)
        try:
            completion = resp["predictions"][0]["candidates"][0]["content"]
        except Exception as e:
            return {"error": {"message": str(e)}}, 0

        message = {"role": "assistant", "content": completion}
        if len(completion) > 2000:
            completion = completion[:2000]
        tlength = resp["metadata"]["tokenMetadata"]["outputTokenCount"]["totalBillableCharacters"] + resp["metadata"]["tokenMetadata"]["inputTokenCount"]["totalBillableCharacters"]
        tokencost = math.ceil((tlength/1000)*.0005)

        return message, tokencost
    
    def LLaMA(model: str, conversation: list[dict], settings: dict = None) -> tuple:
       
        conversationformatted = deepcopy(conversation)
        try:
            if conversationformatted[0]["role"] == "system":
                conversationformatted.pop(0)
        except:
            pass
        print(conversationformatted)
        prompt = "[INST] <<SYS>>\n" + conversation[0]["content"] +  " Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, sexual or illegal content. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n"
        for i in conversationformatted:
            if i["role"] == "user":
                prompt = prompt + i["content"] + "[/INST]"
            elif i["role"] == "function":
                prompt = prompt + i["content"] + "[/INST]"

            elif i["role"] == "assistant":
                prompt = prompt + i["content"] + "[INST]"
            i.pop("role")

            
        print(conversation)
        print(conversationformatted)

        if settings == None:
            settings = {
                "temperature": 1,
                "frequency_penalty": 0,
            }

        data = json.dumps(
            {"input":
                {
                    "prompt": prompt,
                    "max_new_tokens": 500,
                    "temperature": settings["temperature"]/2,
                    "repetition_penalty": settings["frequency_penalty"],
                }}
        )

        headers = {"content-type": "application/json", "authorization": RUNPOD_KEY, "accept": "application/json"}

        try:
            req = requests.post(url="https://api.runpod.ai/v2/k8rzhsihgkntpm/run", data=data, headers=headers)
        except Exception as e:
            return {"error": {"message": str(e)}}, 0
        resp = req.json()
        print(resp)
        try:
            reqid = resp["id"]
        except:
            return {"error": {"message": None}}, 0

        # TODO check
        while resp["status"] in ["IN_PROGRESS", "IN_QUEUE"]:
            time.sleep(2)
            resp = requests.get("https://api.runpod.ai/v2/k8rzhsihgkntpm/status/" + reqid, headers=headers)
            resp = resp.json()
            
            if resp["status"] in ["IN_PROGRESS", "IN_QUEUE"]:
                continue
        if resp["status"] == "FAILED":
            return {"error": {"message": resp}}, 0
        completion = resp["output"]
        timespent = resp["executionTime"]/1000
        cost = 0.00038*timespent
        tokencost = math.ceil(cost*16666)
    

        if len(completion) > 2000:
            completion = completion[:2000]




        return {"role": "assistant", "content": completion}, tokencost
    
    def Replicate(model: str, conversation: list[dict]) -> tuple:
        conversationformatted = deepcopy(conversation)
        try:
            if conversationformatted[0]["role"] == "system":
                conversationformatted.pop(0)
        except:
            pass
        print(conversationformatted)
        prompt = f"""
The following is a conversation with an AI assistant, {chatmodels[model]["name"]}. The assistant is helpful, creative, clever, and very friendly. The human will write in the "Human" space and you will write in the "AI" space. Do not fill in information for the human.

Human: Hi! How are you?
AI: Good. What would you like to talk about today?
        """
        for i in conversationformatted:
            if i["role"] == "user":
                prompt = prompt + "\nHuman: " + i["content"]
            elif i["role"] == "function":
                prompt = prompt + "\nFunction Response: " + i["content"]

            elif i["role"] == "assistant":
                prompt = prompt + "\nAI: " + i["content"]
            i.pop("role")
        
        prompt = prompt + "\nAI:"
            
        print(conversation)
        print(conversationformatted)

        data = json.dumps(
            {"version": chatmodels[model]["version"], 
            "input": {"prompt": prompt, "max_tokens": int((len(prompt)/2)+1000)}}
        )

        headers = {"Content-Type": "application/json", "Authorization": "Token " + REPLICATE_TOKEN}


        try:
            req = requests.post(url="https://api.replicate.com/v1/predictions", data=data, headers=headers)
        except Exception as e:
            return {"error": {"message": str(e)}}, 0
        resp = req.json()
        print(resp)
        try:
            reqid = resp["id"]
        except:
            return {"error": {"message": None}}, 0
        for i in range(0, 30):
            time.sleep(2)
            followup = requests.post(url="https://api.replicate.com/v1/predictions/" + reqid, headers=headers)
            followup = followup.json()
            if followup["status"] == "succeeded":
                break
            if followup["status"] == "failed":
                return {"error": {"message": followup}}, 0

        try:
            print(followup)
        except:
            return {"error": {"message": None}}, 0

        
        
        print(resp)
        try:
            completion = followup["output"]
            completion = ''.join(completion)
            completion = completion.split("Human:")[0]
        except Exception as e:
            return {"error": {"message": str(e)}}, 0

        
        if len(completion) > 2000:
            completion = completion[:2000]
        ptime = followup["metrics"]["predict_time"]
        cost = ptime*0.0023
        tokencost = math.ceil(cost*16666)


        return {"role": "assistant", "content": completion}, tokencost
    

    def Cohere(model: str, conversation: list[dict], settings: dict, documents: list[dict] = None, ) -> tuple:
        conversationformatted = [] 
        for i in conversation:
            if i["role"] == "user" or i["role"] == "function":
                conversationformatted.append({"role": "USER", "message": i["content"]})

            if i["role"] == "assistant":
                conversationformatted.append({"role": "CHATBOT", "message": i["content"]})
            
        print(conversation)
        print(conversationformatted)
        conversationformatted.pop(-1)

        url = "https://api.cohere.ai/v1/chat"
        headers = {"authorization": "Bearer " + COHERE_KEY, "Content-Type": "application/json"}
        data = {
            "message": conversation[-1]["content"],
            "chat_history": conversationformatted,
            "prompt_truncation": "AUTO"
        }

        if settings:
            for i in settings.keys():
                if i == "stop":
                    data["stop_sequences"] = [settings[i]]
                    continue
                data[i] = settings[i]

        if documents:
            data["documents"] = documents

        if conversation[0]["role"] == "system":
            data["preamble_override"] = conversation[0]["content"]

        req = requests.post(url=url, data=json.dumps(data), headers=headers)

        if req.status_code not in [200, 201]:
            return {"error": {"message": req.text}}, 0

        resp = req.json()

        completion = resp["text"]



        
        tokens = resp["token_count"]["billed_tokens"]

        cost = 0.002*tokens/1000
        tokencost = math.ceil(cost*16666)

        response = {"role": "assistant", "content": completion}

        if "citations" in resp.keys():
            response["citations"] = resp["citations"]

        return response, tokencost
    
imagemodels = {
    "kandinsky-v2": {
        "name": "Kandinsky v2.1",
        "endpoint": "/image/generate",
        },
    "sd-anything-v4": {
        "name": "Anything v4",
        "endpoint": "/image/generate",
        },
    "sd-openjourney": {
        "name": "OpenJourney",
        "endpoint": "/image/generate",
        },
    "stable-diffusion-xl-1024-v1-0": {
        "name": "Stable Diffusion XL v1.0",
        "cost": 350,
        "endpoint": "/image/generate",
        },
    "dall-e-2": {
        "name": "DALL-E 2",
        "cost": 500,
        "endpoint": "/image/generate",
        },
    "stable-diffusion-512-v2-1": {
        "name": "Stable Diffusion v2.1",
        "cost": 50,
        "endpoint": "/image/generate",
        },
    "stable-diffusion-xl-beta-v2-2-2": {
        "name": "Stable Diffusion XL v2.2.2 (old)",
        "cost": 50,
        "endpoint": "/image/generate",
        },
    "esrgan-v1-x2plus": {
        "name": "Real-ESRGAN v1.0 Upscaler",
        "cost": 40,
        "endpoint": "/image/upscale",
        }
        

        
}

class Image():
    def Generate(model: str, prompt: str, width: int = 512) -> tuple:
        if model == "dall-e-2":
            data = json.dumps({"prompt":prompt, "size": "1024x1024"})
            try:
                req = requests.post(url="https://api.openai.com/v1/images/generations", data=data, headers={"Authorization": "Bearer " + OPENAI_API_KEY, "Content-Type": "application/json"})
                if req.status_code not in [200, 201]:
                    return {"error": {"message": req.text}}, 0
            
            except Exception as e:
                return {"error": {"message": str(e)}}, 0
                
            resp = req.json()
            print(resp)
            if "error" in resp.keys():
                return {"error": {"message": resp["error"]["message"]}}, 0
            url = resp["data"][0]["url"]

            resp = requests.get(url)
            file = resp.content
            return file, imagemodels[model]["cost"]

        elif model in ["kandinsky-v2", "sd-anything-v4", "sd-openjourney"]:
            
            if model == "kandinsky-v2":
                data = json.dumps(
                {
                    "input": {
                        "prompt": prompt,
                        "negative_prior_prompt": "string",
                        "negative_decoder_prompt": "string",
                        "num_steps": 100,
                        "guidance_scale": 4,
                        "h": width,
                        "w": width,
                        "sampler": "ddim",
                        "prior_cf_scale": 4,
                        "prior_steps": "5",
                        "num_images": 1,
                        "seed": -1
                        
                    }
                }
            )   
            elif model == "sd-anything-v4":
                data = json.dumps(
                {
                    "input": {
                        "prompt": prompt,
                        "width": width,
                        "height": width,
                        "guidance_scale": 7.5,
                        "num_inference_steps": 50,
                        "num_outputs": 1,
                        "prompt_strength": 0.8,
                        "scheduler": "K-LMS"

                    }
                }
            )   
            elif model == "sd-openjourney":
                data = json.dumps(
                {
                    "input": {
                        "prompt": prompt,
                        "width": width,
                        "height": width,
                        "guidance_scale": 7.5,
                        "num_inference_steps": 50,
                        "num_outputs": 1,
                        "prompt_strength": 0.8,
                        "scheduler": "K-LMS"

                    }
                }
            )     
    
            
        

            headers = {"content-type": "application/json", "authorization": RUNPOD_KEY, "accept": "application/json"}

            try:
                req = requests.post(url=f"https://api.runpod.ai/v2/{model}/runsync", data=data, headers=headers)
                if req.status_code not in [200, 201]:
                    return {"error": {"message": req.text}}, 0
            except Exception as e:
                return {"error": {"message": str(e)}}, 0
            resp = req.json()
            print(resp)
            if resp["status"] != "COMPLETED":
                return {"error": {"message": resp}}, 0
            if model == "kandinsky-v2":
                outputurl = resp["output"]["image_url"]
            if model in ["sd-openjourney", "sd-anything-v4"]:
                outputurl = resp["output"][0]["image"]
            try:
                output = requests.get(url=outputurl)
                file = output.content
            except:
                return {"error": {"message": "File download error."}}, 0
            

            ptime = resp["executionTime"]/1000
            cost = ptime*0.00025
            tokencost = math.ceil(cost*16666)
            print(tokencost)
            return file, tokencost
        elif model in ["stable-diffusion-xl-1024-v1-0", "stable-diffusion-512-v2-1", "stable-diffusion-xl-beta-v2-2-2"]:
            data = {
                    "text_prompts": [
                        {
                            "text": prompt
                        }
                    ],
                    "height": width,
                    "width": width,
                    "samples": 1,
                    "steps": 30

                }
            

            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {STABILITY_API_KEY}"
            }

            req = requests.post(
                url=f"https://api.stability.ai/v1/generation/{model}/text-to-image",
                data=json.dumps(data),
                headers=headers

            )
            if req.status_code not in [200, 201]:
                return {"error": {"message": req.text}}, 0
            resp = req.json()
            #print(resp)

            image = resp["artifacts"][0]
            return base64.b64decode(image["base64"]), imagemodels[model]["cost"]
        
    def Upscale(model, image):
        req = requests.post(
            url=f"https://api.stability.ai/v1/generation/{model}/image-to-image/upscale",
            data={"image": image, "width": "2048"},
            
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {STABILITY_API_KEY}"
            },)
        
        resp = req.json()

        if req.status_code not in [200, 201]:

            return {"error": {"message": resp}}, 0
        


        return base64.b64decode(resp["artifacts"][0]["base64"]), 40
    
    def Blip2(image: str, caption: bool = False, question: str = None, context: str = None, temperature: float = 1) -> tuple:
        input = {"image": image, "caption": caption, "question": question, "context": context, "temperature": temperature}
        inputcopy = deepcopy(input)


        
        for i in inputcopy.keys():
            if inputcopy[i] == None:
                input.pop(i)

        data = {"version": "4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608", 
            "input": input}
        
        headers = {"Content-Type": "application/json", "Authorization": "Token " + REPLICATE_TOKEN}

        
        req = requests.post(url="https://api.replicate.com/v1/predictions", data=json.dumps(data), headers=headers)
        print(req.status_code)
        if req.status_code not in [200, 201]:
            return {"error": {"message": req.text}}, 0
        resp = req.json()
        print(resp)
        try:
            reqid = resp["id"]
        except:

            return {"error": {"message": req.text}}, 0
        for i in range(0, 30):
            time.sleep(2)
            followup = requests.post(url="https://api.replicate.com/v1/predictions/" + reqid, headers=headers)
            followup = followup.json()
            if followup["status"] == "succeeded":
                break
            if followup["status"] == "failed":
                return {"error": {"message": followup}}, 0
                return

        try:
            ptime = followup["metrics"]["predict_time"]
            cost = ptime*0.0023
            creditCost = math.ceil(cost*16666)
            return followup["output"], creditCost
        except:
            return {"error": {"message": followup}}, 0
    
videomodels = {
    "damo": {
        "name": "DAMO Text-to-Video",
        "endpoint": "/video/generate",
        "version": "1e205ea73084bd17a0a3b43396e49ba0d6bc2e754e9283b2df49fad2dcf95755"
        },
    "videocrafter": {
        "name": "VideoCrafter",
        "endpoint": "/video/generate",
        "version": "3a7e6cdc3f95192092fa47346a73c28d1373d1499f3b62cdea25efe355823afb"
        },
    "dreamlike": {
        "name": "Dreamlike",
        "endpoint": "/video/generate",
        "version": "e671ffe4e976c0ec813f15a9836ebcfd08857ac2669af6917e3c2549307f9fae", 
        "repo": "dreamlike-art/dreamlike-photoreal-2.0"
        },
    "openjourney": {
        "name": "OpenJourney",
        "endpoint": "/video/generate",
        "version": "e671ffe4e976c0ec813f15a9836ebcfd08857ac2669af6917e3c2549307f9fae",
        "repo": "prompthero/openjourney"
        }
    }

class Video():
    def Generate(model: str, prompt: str, seed: int = random.randint(1, 4294967295), num_frames: int = 16, fps: int = 8) -> tuple:
        if model == "damo":
            
            
            data = json.dumps(
                {"version": videomodels[model]["version"], 
                "input": {"prompt": prompt, "num_frames": num_frames, "fps": fps, "seed": seed}}
            )

            headers = {"Content-Type": "application/json", "Authorization": "Token " + REPLICATE_TOKEN}

            try:
                req = requests.post(url="https://api.replicate.com/v1/predictions", data=data, headers=headers)

            except Exception as e:
                return {"error": {"message": str(e)}}, 0
            resp = req.json()
            print(resp)
            try:
                reqid = resp["id"]
            except:
                return {"error": {"message": str(e)}}, 0
            for i in range(0, 60):
                time.sleep(6)
                followup = requests.post(url="https://api.replicate.com/v1/predictions/" + reqid, headers=headers)
                followup = followup.json()
                if followup["status"] == "succeeded":
                    break
                if followup["status"] == "failed":
                    
                    
                    return {"error": {"message": str(followup)}}, 0

            try:
                print(followup)
            except:
                
                return {"error": {"message": "Timed out."}}, 0
            

            try:
                outputurl = followup["output"]
                output = requests.get(url=outputurl)

            except:
                
                
                return {"error": {"message": str(followup)}}, 0
            
        elif model == "videocrafter":
            
            data = json.dumps(
                {"version": "3a7e6cdc3f95192092fa47346a73c28d1373d1499f3b62cdea25efe355823afb", 
                "input": {"prompt": prompt, "seed": seed}}
            )

            headers = {"Content-Type": "application/json", "Authorization": "Token " + REPLICATE_TOKEN}

            try:
                req = requests.post(url="https://api.replicate.com/v1/predictions", data=data, headers=headers)

            except Exception as e:
                
                return {"error": {"message": str(e)}}, 0
            resp = req.json()
            print(resp)
            try:
                reqid = resp["id"]
            except:
                return {"error": {"message": str(resp)}}, 0
            for i in range(0, 60):
                time.sleep(6)
                followup = requests.post(url="https://api.replicate.com/v1/predictions/" + reqid, headers=headers)
                followup = followup.json()
                if followup["status"] == "succeeded":
                    break
                if followup["status"] == "failed":
                    
                    return {"error": {"message": str(followup)}}, 0

            try:
                print(followup)
            except:
                
                return {"error": {"message": "Timed out."}}, 0
            

            try:
                outputurl = followup["output"]
                output = requests.get(url=outputurl)
            except:
                
                return {"error": {"message": str(followup)}}, 0
            
        elif model in ["dreamlike", "openjourney"]:

            
            data = json.dumps(
                {"version": "e671ffe4e976c0ec813f15a9836ebcfd08857ac2669af6917e3c2549307f9fae", 
                "input": {"prompt": prompt, "video_length": math.ceil(num_frames/fps), "fps":int(fps), "model_name": videomodels[model]["repo"], "seed": seed}}
            )

            headers = {"Content-Type": "application/json", "Authorization": "Token " + REPLICATE_TOKEN}

            try:
                req = requests.post(url="https://api.replicate.com/v1/predictions", data=data, headers=headers)

            except Exception as e:
                return {"error": {"message": str(e)}}, 0
            resp = req.json()
            print(resp)
            try:
                reqid = resp["id"]
            except:
                return {"error": {"message": None}}, 0
            for i in range(0, 60):
                time.sleep(6)
                followup = requests.post(url="https://api.replicate.com/v1/predictions/" + reqid, headers=headers)
                followup = followup.json()
                if followup["status"] == "succeeded":
                    break
                if followup["status"] == "failed":
                    return {"error": {"message": str(followup)}}, 0

            try:
                print(followup)
            except:
                return {"error": {"message": "Timed out."}}, 0
            

            try:
                outputurl = followup["output"]
                output = requests.get(url=outputurl)
            except:
                return {"error": {"message": str(followup)}}, 0
            
        ptime = followup["metrics"]["predict_time"]
        cost = ptime*0.0023
        tokencost = math.ceil(cost*16666)
        return output.content, tokencost
    

class Moderate():
    def OpenAI(text: str) -> tuple:
        mod = json.dumps({"input": text})
        req = requests.post(url="https://api.openai.com/v1/moderations", data=mod, headers={"Authorization": "Bearer " + OPENAI_API_KEY, "Content-Type": "application/json"})
        if req.status_code not in [200, 201]:
            return {"error": {"message": req.text}}, 0
        modreq = req.json()
        if "error" in modreq.keys():
            return {"error": {"message": modreq["error"]["message"]}}, 0
        return modreq, 0

    def Perspective(text: str) -> tuple:

        url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

        data = {

        "comment": {
            "text": text
        },
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {}
        }

        }

        req = requests.post(url, json=data, params={"key": GOOGLE_KEY})
        if req.status_code not in [200, 201]:
            return {"error": {"message": req.text}}, 0
        resp = req.json()
        if "error" in resp.keys():
            return {"error": {"message": resp["error"]["message"]}}, 0
        return resp, 1


class Music():
    def Generate(prompt: str, duration: int = 10):
        url = "https://api.replicate.com/v1/predictions"

        data = {
            "version": "7a76a8258b23fae65c5a22debb8841d1d7e816b75c2f24218cd2bd8573787906", 
            "input": {
                "model_version": "melody",
                "prompt": prompt,
                "duration": duration
            }
        }
        headers = {
            "Authorization": "Token " + REPLICATE_TOKEN,
        }

        req = requests.post(url, json=data, headers=headers)

        resp = req.json()

        print(resp)
        try:
            reqid = resp["id"]
        except:
            return {"error": {"message": None}}, 0
        for i in range(0, 30):
            time.sleep(2)
            followup = requests.post(url="https://api.replicate.com/v1/predictions/" + reqid, headers=headers)
            followup = followup.json()
            if followup["status"] == "succeeded":
                break
            if followup["status"] == "failed":
                return {"error": {"message": followup}}, 0

        try:
            print(followup)
        except:
            return {"error": {"message": None}}, 0
        

        try:
            outputurl = followup["output"]
            output = requests.get(url=outputurl)
        except:
            
            return {"error": {"message": str(followup)}}, 0
        ptime = followup["metrics"]["predict_time"]
        cost = ptime*0.001150
        tokencost = math.ceil(cost*16666)
        return output.content, tokencost
    


class Speech():
    def GetTTSVoices():
        credentials.refresh(google.auth.transport.requests.Request())
        req = requests.get("https://texttospeech.googleapis.com/v1/voices", headers={"Content-Type": "application/json", "Authorization": "Bearer " + str(credentials.token), "x-goog-user-project": "chatgptdiscord"})
        resp = req.json()
        return resp
    def tts(text: str, voice: dict = {
                "languageCode": "en-us",
                "name": "en-US-Standard-A",
                "ssmlGender": "MALE"
            }):

        data = {
            "input": {
                "text": text
            },
            "voice": voice,
            "audioConfig": {
                "audioEncoding": "MP3"
            }
        }

        credentials.refresh(google.auth.transport.requests.Request())
            #print(credentials.token)
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + str(credentials.token), "x-goog-user-project": "chatgptdiscord"}

        req = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize", data=json.dumps(data), headers=headers)

        if req.status_code not in [200, 201]:
            return {"error": {"message": req.text}}, 0
        resp = req.json()
        b64 = resp["audioContent"]
        creditcost = math.ceil(len(text.encode('utf-8'))*.2666)
        return b64, creditcost
        