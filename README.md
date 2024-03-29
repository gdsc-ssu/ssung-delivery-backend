# SSUNG-DELIVERY-BACKEND
![image](https://user-images.githubusercontent.com/46417868/230830852-8a8f9f31-80c8-47e3-8ae6-c14de98a821b.png)
[Whole Project Introduction](https://github.com/gdsc-ssu/ssung-delivery)

## 🛠️ Technology & Architecture
<img width="546" alt="Screenshot 2023-04-10 at 14 07 38" src="https://user-images.githubusercontent.com/46417868/230830260-92bae2e4-6d09-49a9-9322-b3301f06143e.png">
Our team chose FastAPI as the backend framework for our project due to its ease of use in building APIs and its support for asynchronous processing, allowing for efficient backend system development. Additionally, FastAPI is written in Python, which provides advantages in code reproducibility and development speed.
<br/><br/>
We also utilized Docker containers for easy environment management and Cloud Run for quick deployment. For our relational database needs, we chose to use Google Cloud SQL, which allowed us to leverage its features such as automated backups and scalability. Finally, we used various GCP services such as Cloud Build and Artifact Registry for streamlined container image management.
 <br/><br/>

| Tech Spec | Description                                                                                                                                                                                                                                       |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cloud Run | <ul><li>Fast deployment</li><li>Easy environment management through Docker</li><li>Built-in CI/CD features</li><li>Serverless architecture to reduce server costs</li><li>Use Artifact Registry for Docker image storage and versioning</li></ul> |
| Cloud SQL | <ul><li>Delivery data has a predefined schema.</li><li>Best option for managing data in a structured manner in the GCP environment.</li></ul>                                                                                                     |
| FastAPI   | <ul><li>Easiest framework for building APIs</li><li>Provides efficient backend system construction with asynchronous processing logic</li><li>Utilizes Python, enabling code reproducibility and fast development speed</li></ul>                 |

## 🔑 Key Implementations

### Word Identifer

Word identifiers are a combination of words used to identify information instead of serial numbers. They are easier to remember and understand, and more secure than traditional identifiers.
<br/><br/>
They can be useful in situations where serial numbers may not be appropriate and offer a more user-friendly option. Additionally, word identifiers can be made even more secure by using random combinations of words. They provide an alternative to traditional identifiers and can be particularly useful in situations that handle sensitive information.

#### Work Flow
![image](https://user-images.githubusercontent.com/46417868/230830515-10800750-01bf-4242-8d7e-0e618fd5beb7.png)

#### Flow

- Create
    1. The user registers the shipping information.
    2. The server randomly extracts 3 words from the word DB.
    3. Combine the 3 extracted words into one string.
    4. Encodes the combined string into Base64.
    5. Run a duplicate check to see if the encoded string already exists in the DB.
    6. If not duplicated, store the encoded string in the DB with the shipping information.
    7. Repeat steps 2 through 5 if duplicated.
- Read
    1. The user enters a word identifier.
    2. The encoder inside the service encodes the user-entered word identifier into Base64.
    3. Get the order information by sending a query to the DB with the encoded value.
    4. Show the imported order information to the user.

## 📌 Going Forward

We will introduce golang and gRPC additionally.

- [ ]  golang - Enable efficient and reliable programming language
- [ ]  gRPC - Enables rapid data transfer and scalable service development
