ROADMAP = {

    "Python": "Learn Python fundamentals, functions, OOP and file handling.",

    "SQL": "Learn SQL queries, joins, grouping, subqueries and database operations.",

    "Excel": "Learn Excel formulas, pivot tables, charts and data cleaning.",

    "Pandas": "Learn DataFrames, data cleaning, filtering, grouping and merging.",

    "NumPy": "Learn arrays, indexing, mathematical operations and numerical computing.",

    "Power BI": "Learn dashboards, Power Query, data modeling and visualization.",

    "Machine Learning": "Learn supervised and unsupervised learning algorithms.",

    "Scikit-learn": "Learn preprocessing, model training, evaluation and pipelines.",

    "FastAPI": "Learn REST API development using FastAPI and Python.",

    "Docker": "Learn containers, Dockerfiles, images and container deployment.",

    "Git": "Learn Git commands, branches, commits and GitHub workflows.",

    "Deep Learning": "Learn neural networks, backpropagation and deep learning frameworks.",

    "PyTorch": "Learn tensors, neural networks, training loops and model deployment.",

    "TensorFlow": "Learn neural networks, model training and TensorFlow workflows.",

    "LLM": "Learn large language models, prompting and LLM application development.",

    "RAG": "Learn embeddings, vector databases and retrieval augmented generation.",

    "APIs": "Learn REST APIs, HTTP methods, JSON and API integration.",

    "NLP": "Learn tokenization, text preprocessing, embeddings and language models.",

    "NLTK": "Learn text preprocessing, tokenization, stemming and NLP analysis.",

    "spaCy": "Learn NLP pipelines, named entity recognition and text processing.",

    "Transformers": "Learn transformer architecture, attention and pretrained models.",

    "Hugging Face": "Learn how to use pretrained NLP and AI models.",

    "OpenCV": "Learn image processing, video processing and computer vision operations.",

    "CNN": "Learn convolutional neural networks for image classification.",

    "YOLO": "Learn object detection and real-time computer vision using YOLO.",

    "Computer Vision": "Learn image processing, feature extraction and object detection.",

    "Flask": "Learn Flask routing, templates, APIs and backend development.",

    "Django": "Learn Django models, views, URLs and web application development.",

    "JavaScript": "Learn JavaScript fundamentals, DOM manipulation and asynchronous programming.",

    "React": "Learn React components, state, props and API integration.",

    "Node.js": "Learn backend development and REST APIs using Node.js.",

    "MongoDB": "Learn NoSQL databases, collections, documents and CRUD operations.",

    "PostgreSQL": "Learn relational database concepts and PostgreSQL queries.",

    "AWS": "Learn basic cloud computing, EC2, S3 and deployment.",

    "Azure": "Learn Azure fundamentals and cloud application deployment.",

    "Google Cloud": "Learn Google Cloud fundamentals and application deployment.",

    "Jenkins": "Learn CI/CD pipelines and automated software deployment.",

    "Linux": "Learn Linux commands, file management and system administration.",

    "REST API": "Learn REST architecture, HTTP methods and API development.",

    "OOP": "Learn classes, objects, inheritance, polymorphism and encapsulation.",

    "Data Structures": "Learn arrays, linked lists, stacks, queues, trees and hash tables.",

    "Algorithms": "Learn searching, sorting, recursion and algorithmic problem solving.",

    "DSA": "Practice arrays, strings, linked lists, stacks, queues, trees and algorithms."
}


def generate_roadmap(missing_skills):

    roadmap = []

    for index, skill in enumerate(missing_skills):

        explanation = ROADMAP.get(
            skill,
            f"Learn the fundamentals and practical applications of {skill}."
        )

        week = (index // 2) + 1

        roadmap.append({
            "Week": f"Week {week}",
            "Skill": skill,
            "Learning Goal": explanation
        })

    return roadmap