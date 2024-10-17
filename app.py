from flask import Flask, request, jsonify, render_template
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Google API key for generative AI
genai.configure(api_key=os.getenv("AIzaSyBIkFUb4luUnTWeOTzt-R_h5NNGLdvdlPs"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html')

@app.route('/pest-control')
def pest_control():
    return render_template('pest-control.html')

# Endpoint to handle image and input text
@app.route('/analyze', methods=['GET', 'POST'])
def analyze_image():
    if request.method == 'GET':
        # Render the HTML form when the route is accessed via GET
        return '''
            <html>
            <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }

                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }

                    h1 {
                        color: #2c3e50;
                    }

                    form {
                        display: flex;
                        flex-direction: column;
                    }

                    label {
                        font-weight: bold;
                        margin-bottom: 5px;
                    }

                    input, button {
                        padding: 10px;
                        margin-bottom: 15px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }

                    button {
                        background-color: #2c3e50;
                        color: white;
                        cursor: pointer;
                    }

                    button:hover {
                        background-color: #34495e;
                    }
                </style>
                    
                <body>
                    <h1>Plant Disease Analysis</h1>
                    <form method="POST" enctype="multipart/form-data" action="/analyze">
                        <label for="input_text">Input Text:</label>
                        <input type="text" id="input_text" name="input_text"><br><br>
                        <label for="image">Upload Image:</label>
                        <input type="file" id="image" name="image" accept="image/*"><br><br>
                        <button type="submit">Analyze Image</button>
                    </form>
                </body>
            </html>
        '''
    elif request.method == 'POST':
        try:
            # Get the input text and image from the request
            input_text = request.form.get('input_text')
            image_file = request.files['image']

            # Check if an image file was uploaded
            if image_file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            # Print input text and image filename for debugging
            print(f"Input Text: {input_text}")
            print(f"Uploaded Image: {image_file.filename}")

            # Open the image using PIL
            image = Image.open(image_file)

            # Process the image and input text with generative AI
            response_text = get_gemini_response(input_text, image)

            # Return the AI response as JSON
            return f"""
            <html>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }}

                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}

                    h1 {{
                        color: #2c3e50;
                    }}

                    form {{
                        display: flex;
                        flex-direction: column;
                    }}

                    label {{
                        font-weight: bold;
                        margin-bottom: 5px;
                    }}

                    input, button {{
                        padding: 10px;
                        margin-bottom: 15px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }}

                    button {{
                        background-color: #2c3e50;
                        color: white;
                        cursor: pointer;
                    }}

                    button:hover {{
                        background-color: #34495e;
                    }}
                </style>
                <body>
                    <h1>Plant Disease Analysis</h1>
                    <p>Input Text: {input_text}</p>
                    <p>Uploaded Image: {image_file.filename}</p>
                    <p>AI Response: {markdown.markdown(response_text)}</p>
                </body>
            </html>
            """

        except Exception as e:
            print(f"Error: {str(e)}")  # Print the error for debugging
            return jsonify({"error": str(e)}), 500

# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_template = """
        Analyze the image to determine if it is related to plants or leaves:

        1. Identify the botanical and common names.
        2. Detect diseases and suggest treatments.
    """

    # Create the prompt based on input_text
    final_prompt = f"{input_text}\n\n{prompt_template}" if input_text else prompt_template
    
    # Generate a response using the model
    response = model.generate_content([final_prompt, image])
    
    return response.text

if __name__ == '__main__':
    app.run(debug=False)
