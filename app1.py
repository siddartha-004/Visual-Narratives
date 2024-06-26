import os
import requests
import streamlit as st

# create a .env file in your project directory and add your hugging face token as:
# HF_API_KEY = "hf_your_token"
# after that uncomment below two lines of code to load the hf api token

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('HF_API_KEY')

headers = {"Authorization": f"Bearer {API_KEY}"}



def image_to_text(image_source):
	salesforce_blip = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
	
	API_URL = salesforce_blip

	with open(image_source, "rb") as f:
		data = f.read()

	response = requests.post(API_URL, headers=headers, data=data)
	response =  response.json()

	#error handling
	try:
		return response[0]["generated_text"]
	except Exception as e:
		# print(e)
		# print(f"\n\n{str(e)}\n\n")
		return "error"


def generateStory(inputText):
	# print(inputText)
	#handling error of image_to_text model
	if inputText == "error":
		return "Please accept our apology as an error has been occured in the server. Please wait for a while!!"
	# gpt2_xl = "https://api-inference.huggingface.co/models/gpt2-xl"

	#using "falcon 7b instruct" as it is working way better than gpt2 for creating stories
	falcon_7b = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

	API_URL = falcon_7b

	falcon_text_for_story = f"create a positive, real, practical and short story from this context {inputText}."

	payload = {
				"inputs": falcon_text_for_story,
				"parameters": {
								# "max_length": 2,
								"max_new_tokens": 250,
								"do_sample":True,
								# "max_time": 15.00,
								"top_k": 10,		#total words in text
								"temperature": 1,
								# "repetition_penalty": 80,
								"return_full_text": False,
							  },
				"options": {
							"wait_for_model": True
						   }
			  }
	# print(payload["inputs"])
	
	response = requests.post(API_URL, headers=headers, json=payload)
	response = response.json()

	# print(type(response))
	# print(response,"\n\n")

	# response = {'error': 'Model gpt2-large is currently loading', 'estimated_time': 129.88461303710938} 
	# response = {'error': 'Internal Server Error'}

	#  error handling
	try:
		return response[0]["generated_text"]
	except Exception as e:
		# print(e)
		# print(f"\n\n{str(e)}\n\n")
		return "Please accept our apology as an error has been occured in the server. Please wait for a while!!"


def imageToStory():
	st.set_page_config(page_title = "Photo to story", page_icon="👾")
	# emoji shortcut: CTRL + CMD + Space

	#Removing the Menu Button and Streamlit Icon
	hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
	st.markdown(hide_default_format, unsafe_allow_html=True)

	st.title("Photo to story")
	st.header("Turn your photos into a beautiful story")
	st.subheader("Bored of your regular photos...I have a solution for you. Turn your most favourite photos into a \
					beautiful story. Just browse your photo and hit enter and see the magic 🪄")
	st.subheader("Don't worry about your privacy! This app doesn't store anything. Your photo is deleted \
					right after the story is generated🔐")

	# sidebar
	
	linkedin = "https://www.linkedin.com/in/priyansh-bhardwaj-25964317a"
	about_developer = "**Priyansh Bhardwaj**"

	#tech stack
	with st.sidebar.expander("**Tech stack**"):
		st.write('''
			- **LLM : falcon-7b-instruct**
			- **HuggingFace**
			- **Langchain**'''
				)
	
	#app working
	with st.sidebar.expander("**App Working**"):
		st.write('''
			**Photo to Story: Transform Your Photos into Captivating Narratives with Ease.**
			''')
		st.write('''
			- **Upload Your Photo:** Select any photo that sparks your imagination.
			- **Caption Generation:** We employ a Hugging Face model to generate a suitable caption for your image. This step sets the stage for your story.
			- **Falcon 7B Unleashed:** With the generated caption in hand, we turn to Falcon 7B, our powerful large language model. It takes your caption and transforms it into a real, interesting, and short story.
			- **Enjoy Your Story:** Your photo is now more than just an image; it's a doorway to a unique narrative experience.
			- **Privacy Priority:** We respect your privacy. Your uploaded photos are used solely for caption generation and are promptly deleted after the process is complete.
		''')
		st.write("Unlock the power of 'Photo to Story' and let your pictures speak volumes with intriguing tales. Your memories will never look the same.")
	
	#about me
	with st.sidebar.expander("**About me**"):
		st.write(about_developer)
		st.write("[Website](https://priyansh-portfolio.streamlit.app/)")
		st.write("[LinkedIn](%s)" %linkedin)

	uploaded_file = st.file_uploader("choose your photo...", type = ["jpg","png"])

	if uploaded_file is not None:
		bytes_data = uploaded_file.getvalue()
		image_path = "images/"+uploaded_file.name 

		with open(image_path, "wb") as file:
			file.write(bytes_data)
		st.image(uploaded_file, caption="Photo successfully uploaded", use_column_width=True)

		if st.button("Generate Story🪄",
					type="primary",
					help="Click this button to generate a story from your photo"):
			
			with st.spinner('Generating Story'):
				caption = image_to_text(image_path)
				# print(f"\n\ncaption: {caption}\n\n")
				story = generateStory(caption)
				# print(f"\n\nstory: {story}\n\n")

			#deleting the images
			for image in os.listdir("images/"):
				file_path = os.path.join("images/", image) 
				os.remove(file_path)

			# with st.expander("Photo caption"):
			# 	st.write(caption)
			# with st.expander("Story"):

			# st.write(caption)
			st.write(story)
		

if __name__ == "__main__":
	imageToStory()