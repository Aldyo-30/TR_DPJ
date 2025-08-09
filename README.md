# Connect with API

This project is a Python-based web application that connects to an **external API** and dynamically displays the retrieved data through a clean and responsive web interface.

## Demo
Run the application at your locall device and access it in your browser :

```
exemple

http://localhost:5000
```


## Features
- Connects the application to an external API
- Uses **Postman** to test and connect to the API
- Displays fetched data on a web interface
- Responsive design using HTML, CSS, and JavaScript
- Clear separation between backend and frontend

## Project Structure
```
TR_DPJ/
│
├── app.py               # Main application file
├── requirements.txt     # Python dependencies
│
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/           # HTML templates (Jinja2)
│   ├── index.html
│   └── layout.html
│
└── README.md            # Project documentation
```

## Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Aldyo-30/TR_DPJ.git
   cd TR_DPJ
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access in browser**
   ```
   http://localhost:5000
   ```

## Using Postman for API Connection
This project utilizes **Postman** to test, debug, and interact with the external API before integrating it into the application.

**Steps to use Postman:**
1. Install [Postman](https://www.postman.com/downloads/)
2. Open Postman and create a new request
3. Set the method (GET, POST, etc.) and API endpoint URL
4. Send the request and review the response
5. Use the tested endpoint and parameters in `app.py` for live integration

## License
This project is intended for learning and development purposes. Feel free to modify and adapt as needed.
