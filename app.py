import os
from openai import OpenAI
import gradio as gr
import re
import uuid
import chromadb
from pprint import pprint
import requests
import random
import json
#-------------------------------------------------
# Setup
#-------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")
client = OpenAI()

#--------------------------------------------------
# Documents #
#--------------------------------------------------
document_overview = """
Name: Shruti Vargantwar

Location: Philadelphia, PA (relocated from Frisco, TX)

Contact: shruti.vargantwar@gmail.com | (913) 202-9581 | linkedin.com/in/shrutivargantwar

Work authorization: US Permanent Resident (Green Card holder) — no sponsorship needed.

Current status: Senior Full-Stack Software Engineer with 13+ years of experience, actively interviewing for senior / lead engineering roles.

Education: Shruti holds an M.S. in Computer Science from UNC Charlotte, where she graduated with a 4.0 GPA after attending from 2010 to 2012. She also holds a B.E. in Computer Science from Savitribai Phule Pune University, India, which she completed from 2005 to 2009.

Certification: Shruti is an AWS Certified Cloud Practitioner.

Thirteen years across healthcare and telecom, building complex, multi-stakeholder workflow systems where business rules, payment flows, and operational reliability all have to work together. That's the common thread — coordination across multiple parties and workflows is where Shruti does her best work, and it's the kind of problem she is looking for next.

T-Mobile | Software Engineer, Order Management (Jan 2022 – Mar 2026) | Frisco, TX

Shruti worked at T-Mobile as a Software Engineer on the Order Management team from January 2022 through March 2026 in Frisco, Texas. She worked on the ET Order Management platform and the Manual Order Portal (MOP), an enterprise B2B order platform covering the full lifecycle from order capture in the user interface through validation, orchestration across billing, provisioning, and SAP, and final fulfillment. She also served as an Interim Team Lead.

Shruti worked as a full-stack engineer, using Angular and TypeScript on the front end and Java and Spring Boot microservices on the back end.

Shruti worked on the Mixed Cart capability using Angular. This capability allowed business customers to buy IoT connectivity, packaged software, and devices in a single order instead of creating one order per product type. She stepped in as interim UI lead when the previous lead left right before the project kickoff. She pulled loaner developers from a sister team while interviewing for the permanent role. The project was shipped on time, and the fallout rate dropped. Shruti received a $3,500 Spot Bonus for this work.

Shruti led a Camunda migration that moved orchestration rules from Drools-based Excel sheets embedded in the validation service to DMN decision tables stored in Git. The new architecture introduced BPMN workflows and an independently deployable orchestration service. The migration reduced rule change lead time from days to hours. It also improved troubleshooting because SDETs went from identifying that "the plan is wrong" to identifying the specific attribute causing the failure. Shruti received a Star Performer Award for this work.

Shruti worked on the migration from Azure Event Hub to Azure Service Bus. The new messaging architecture used a topic-subscription model, Peek-Lock message processing, dead-letter queues with MaxDeliveryCount set to 3, idempotent consumers using correlation IDs, and session-based FIFO processing. The migration eliminated duplicate order creation and resulted in an approximately 35% improvement in reliability. Shruti load-tested the system at approximately 140 messages per minute across five Submit Order instances.

Shruti also designed a Blue-Green messaging strategy using a Service Bus Manager component. The strategy supported drain-before-cutover and allowed the system to roll back in seconds instead of hours.

The T-Mobile Order Management architecture followed an API-first and headless approach. Validate Order served as the single synchronous entry point for all channels, including Salesforce, partner portals, eCommerce, and MOP. Validate Order pre-validated and enriched orders, generated the Order ID, built a Camunda orchestration plan, published an OrderSubmitted event to Service Bus, and returned quickly. Submit Order consumed the event asynchronously.

The architecture used the Saga pattern throughout the order processing workflow. There was no two-phase commit anywhere in the architecture. Failed orders were moved to a Fallout state for controlled replay.

Shruti also worked on payments and security. She implemented risk-based routing between Pay Now and Defer Payment using an internal risk-scoring API. She implemented BIN lookup using the first six digits of a card number. Card data was encrypted client-side before reaching the application servers. CVV was never stored or logged.

Shruti implemented a centralized sensitive-attribute registry with a logging interceptor that automatically masked fields identified as sensitive.

Shruti led the Manual Order Portal's security evolution from hardcoded Apigee credentials in Angular source code to Docker environment variables and ultimately to a Zero Trust Node.js proxy. The proxy validated Okta JWTs and retrieved secrets from Azure Key Vault at runtime. She also implemented MSAL/Azure AD RBAC and route guards.

Shruti worked on product catalog filtering and moved heavy client-side filtering to the server side. She influenced the Product Catalog team to extend its API and refactored the UI using the Factory and Strategy design patterns. The architecture was motivated by a segment-by-transaction-type matrix rather than by personal preference.

Other work at T-Mobile included bulk ordering, eSIM ordering, upgrading Angular from version 9 to version 17, RestTemplate refactoring, and DEEP (Digital Enterprise Event Platform) integration.

Shruti received several recognitions at T-Mobile, including a Star Performer Award, an Ingenious of the Month Award for Connected Car Bundle 2, and a $3,500 Spot Bonus for Mixed Cart. She also mentored T-Mobile employees as well as onshore and offshore contractors.

Cerner Corp (now Oracle Health) | Alternative Payment Manager (Nov 2018 – Dec 2021) | Kansas City, MO

Shruti worked at Cerner Corporation, now Oracle Health, as an Alternative Payment Manager from November 2018 through December 2021 in Kansas City, Missouri.

She built a full-stack claims management platform for a large hospital system specializing in organ transplants. A transplant involves multiple providers, each submitting their own claim. The Alternative Payment Manager platform acted as an intermediary by bundling claims, submitting them to the payer, collecting payment, and redistributing reimbursements back to the participating providers.

Shruti developed Java REST services that integrated with an enterprise pricing engine for bundled episodes of care. She owned defect triage and application support and introduced BDD testing, which doubled Ruby code coverage. She supported weekly CI/CD releases using Jenkins, Spinnaker, and Docker.

Her technology stack included Java, Hibernate, MySQL, Ruby on Rails, and AWS.

Cerner | MyJarvis Portal (Dec 2014 – Oct 2018) | Bengaluru, India

Shruti worked at Cerner on the MyJarvis Portal from December 2014 through October 2018 in Bengaluru, India.

The MyJarvis Portal replaced a manual 15-hour Excel import process and a slow MySQL search across more than 10 million test plan records. Shruti developed an automated keyword extraction tool and an Elasticsearch-backed search engine that reduced analyst search time by approximately 50%.

She extended the portal to support change request and requirements searches. She also developed a similarity engine to identify redundant test coverage. Shruti led a team of developers through the design and delivery of these capabilities and received an Excellence Award.

Her technology stack included Python, Django, PHP/Yii, jQuery, and Elasticsearch.

Cerner | CareAware Multimedia (Sept 2012 – Nov 2014) | Kansas City, MO

Shruti worked at Cerner on CareAware Multimedia from September 2012 through November 2014 in Kansas City, Missouri.

CareAware Multimedia was a clinical portal for physicians and nurses. Shruti built the image annotation feature in CareAware Multimedia Manager and developed REST APIs using IBM WebSphere. She also contributed to a secure framework for handling sensitive medical records.

Her technology stack included VB 6.0, C#, and Java.

Additional info:

- Shruti was in high school in India, where she developed an early interest in computer science and programming. She was also actively pursuing classical dance Kathak and was a member of the school dance team.
- Shruti enjoys cooking and often experiments with new recipes in her free time.
- Shruti is a vegetarian and often cooks with tofu as a protein source.
- Shruti has a particular fondness for Indian and Thai cuisine, often exploring traditional dishes from these cultures.
"""

document_education = """
Education
Maharashtra Institute of Technology College of Engineering

Bachelor of Engineering (B.E.), Computer Engineering

University of North Carolina at Charlotte logo
University of North Carolina at Charlotte

Master of Science (MS), Computer Science
"""

document_professional_experience = """
Experience

T-Mobile logo
Software Engineer

T-Mobile · Full-time

Jan 2022 - Mar 2026 · 4 yrs 3 mos

Frisco, Texas, United States · Hybrid

- As Interim Team Lead, contributed to the design and implementation of customer order workflows supporting new product purchases, plan changes, bundled offerings, and enterprise provisioning across a microservices architecture. Recognized with a Spot Bonus Award.
- Built full stack features across the application: developed Angular/TypeScript UI components and shared libraries for enterprise order portals, along with Java/Spring Boot microservices for order validation, submission, and downstream integrations.
- Contributed to a migration from Event Hub to Azure Service Bus, incorporating dead-letter queues, duplicate detection, and retry policies, which reduced message loss and improved order reliability and traceability.
- Helped lead a migration from Excel-based Drools rule management to a Camunda-driven orchestration engine using DMN decision tables, resulting in a more configurable and maintainable rules service.
- Mentored and supported T-Mobile employees and onshore/offshore contractors to help bridge capability gaps and support delivery of key initiatives.

Skills/Tools: Java, Spring Boot, MongoDB, TypeScript, Angular, Azure Service Bus, Camunda, Git, JUnit

Cerner Corporation logo
Software Engineer II

Cerner Corporation · Full-time

Nov 2018 - Dec 2021 · 3 yrs 2 mos

Kansas City Metropolitan Area · On-site

- Designed and developed Java REST services processing claims, provider transactions, and payer remits while integrating with an enterprise pricing engine to determine reimbursement amounts for bundled episodes of care.
- Owned team's defect triage and support process, resolving client issues efficiently while maintaining development timelines; introduced BDD testing that doubled Ruby code coverage; and supported weekly CI/CD releases across Dev, Staging, and Production environments using Jenkins, Spinnaker, and Docker.
- Mentored new engineers and assisted them with technical queries.

Skills/Tools: Java, Hibernate, SQL, HTML, CSS, JavaScript, React, Ruby on Rails, AWS, Git, Mockito, JUnit, RSpec, Capybara, Selenium

Senior Software Engineer (Associate)

Cerner Healthcare Solutions Private Limited · Full-time

Dec 2014 - Oct 2018 · 3 yrs 11 mos

Bengaluru, Karnataka, India · On-site

- Replaced a manual 15-hour Excel-based import and slow MySQL search across 10 million test plan records by building an automated keyword extraction tool and Elasticsearch-backed search engine, reducing search turnaround time by 60%; extended the same framework to Change Request and Service Request search, and developed a test plan similarity engine to reduce redundant coverage; scaled the solution from a single-team pilot to 20+ solution teams. Recognized with an Excellence Award.
- Led and supervised a team of developers through design, implementation, and delivery of these platform improvements, collaborating directly with test analysts to iterate on search quality and translate end-user feedback into technical solutions.

Skills/Tools: Python, Django, PHP, Yii, jQuery, JavaScript, HTML, CSS, Git, SQL, Elasticsearch

Cerner Corporation logo
Software Engineer

Cerner Corporation · Full-time

Sep 2012 - Nov 2014 · 2 yrs 3 mos

Kansas City Metropolitan Area · On-site

- Developed the image annotation feature within CareAware Multimedia Manager, a clinical portal used by physicians and nurses to view, annotate, and manage patient multimedia objects; built and deployed REST APIs on IBM WebSphere to expose object retrieval functionality, tested via Postman.
- Contributed to a secure framework for handling sensitive medical records by implementing monitoring timers, resolving defects in C# code, and validating functionality through black-box testing using HP Quality Center.
- Participated in functional design, coding, testing, and troubleshooting; created design documents and participated in code reviews using Crucible.

Skills/Tools: VB 6.0, C#, Java, IBM WebSphere
"""

#--------------------------------------------------
# Chunking Function
#--------------------------------------------------
_SENTENCE_END = re.compile(r'[.!?][)"\']?\s')

def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks, preferring natural boundaries.

    Each chunk is at most `chunk_size` characters and overlaps the previous
    one by `overlap` characters. When a chunk would end mid-sentence or
    mid-paragraph, the cut moves back to the nearest natural boundary
    (paragraph break, newline, sentence end, then space, in that order),
    but only if that boundary is past the halfway point of the chunk.

    Returns a list of chunk strings.
    """
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = start + chunk_size

        if end >= n:
            chunks.append(text[start:n])
            break

        min_cut = start + chunk_size // 2
        cut = _find_boundary(text, min_cut, end)

        chunks.append(text[start:cut])
        start = cut - overlap

    return chunks


def _find_boundary(text, min_cut, end):
    """Return a cut index in [min_cut, end], preferring natural boundaries."""
    window = text[min_cut:end]

    idx = window.rfind("\n\n")          # 1. paragraph break
    if idx != -1:
        return min_cut + idx + 2

    idx = window.rfind("\n")            # 2. single newline
    if idx != -1:
        return min_cut + idx + 1

    matches = list(_SENTENCE_END.finditer(window))   # 3. sentence end
    if matches:
        return min_cut + matches[-1].end()

    idx = window.rfind(" ")            # 4. space
    if idx != -1:
        return min_cut + idx + 1

    return end                        # no boundary: hard cut


#--------------------------------------------------
# RAG: Chunk, Embed & Store in ChromaDB
#--------------------------------------------------

documents = [
    {"text": document_overview, "source": "Overview"},
    {"text": document_education, "source": "Education"},
    {"text": document_professional_experience, "source": "Professional Experience"},
]

chunks = []
ids = []
metadatas = []

for doc in documents:
    # Prepare the lists
    chunks_ = split_text_into_chunks(doc["text"], chunk_size=300, overlap=30)
    ids_ = [str(uuid.uuid4()) for _ in range(len(chunks_))]
    metadatas_ = [{"source": doc["source"], "chunk_index": i} for i in range(len(chunks_))]
    # Add to main lists
    chunks.extend(chunks_)
    ids.extend(ids_)
    metadatas.extend(metadatas_)

# Print for logs
print(f"Created {len(chunks)} chunks:\n")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} (ID: {ids[i]}, Source: {metadatas[i]['source']}, Index: {metadatas[i]['chunk_index']}, Length: {len(chunk)}):")
    print(chunk)
    print()
    
#Generate embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)
embeddings = [item.embedding for item in response.data]

# Verify embeddings for logs
print(f"Generated {len(embeddings)} embeddings.")
print(f"Each embedding has {len(embeddings[0])} dimensions.")

# Initialize ChromaDB and Store Vectors

# Initialize ChromaDB client(persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")

# Initialize ChromaDB client (in-memory storage)
#chroma_client = chromadb.Client()
# Get or create + empty the collection before adding new data (for testing purposes)
collection = chroma_client.get_or_create_collection(name="digital_twin", metadata={"description": "Shruti Vargantwar's professional profile and work experience"})
#Empty the collection before adding new data (for testing purposes)
if(collection.get()["ids"]):
    collection.delete(ids=collection.get()["ids"])

# Adding data to ChromaDB
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas
)
pprint(collection.get())

#--------------------------------------------------
# Tools
#--------------------------------------------------
tools = []
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

# Create send_notification function
def send_notification(message: str):
    if pushover_user is None or pushover_token is None: # Handling of potential missing environment variables for Pushover
        return "Notification failed. Pushover not configured."
    payload = {
        "token": pushover_token,
        "user": pushover_user,
        "message": message
    }
    requests.post(pushover_url, data=payload)
    return f"Notification sent: {message}"


# Describe Pushover as an LLM tool
send_notification_function = {
    "name": "send_notification",
    "description": "Sends a push notification to the real Shruti. Use this when: 1) Someone wants to get in touch, hire, or collaborate\
        - ask for their name and contact details first, then send notification to Shruti with the name and contact details. \
        2) You don't the answer to a question about Shruti - send AUTOMATICALLY without asking, include the question so we can add this info to the knowledge base later.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The notification message to send to the  user's device."
            }
        },
        "required": ["message"]
    }
}

# Add Pushover to the list of tools for the LLM
tools.append({"type": "function", "function": send_notification_function})

# Simulates rolling a single six-sided die
def dice_roll():
    return random.randint(1, 6)

# Describe the function for the LLM
roll_dice_function = {
    "name": "dice_roll",
    "description": "Simulates rolling a single six-sided die and returns the result. Use this when the user wants to roll a die for games, decision making, or random number generation.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

# Add the function to list of tools for the LLM
tools.append({"type": "function", "function": roll_dice_function})

#--------------------------------------------------
# Tool Handler
#--------------------------------------------------
def handle_tool_call(tool_calls):
    # Handle all the tool calls in the list
    tool_results = []

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        #print(f"Calling function: {function_name}") # For future debugging

        # Route to the appropriate function based on the function name
        if function_name == "send_notification":
            content = send_notification(args["message"])
        elif function_name == "dice_roll":
            content = f"Rolled: {dice_roll()}"
        #elif function_name == "insert_function_3":
            #content = insert_function_3(args)"
        else:
            content = f"Unknown function {function_name}."
            
        tool_call_result = {
            "role": "tool",
            "content": content,
            "tool_call_id": tool_call.id,
        }
        tool_results.append(tool_call_result)

    return tool_results

#--------------------------------------------------
# System Message
#--------------------------------------------------
system_message = """
You are a digital twin of Shruti Vargantwar. When people talk to you, you respond AS Shruti would — in first person, using her voice, personality and knowledge.
Here is the information about Shruti Vargantwar to help you embody her:

Important: Do not make up things up. If you don't know an answer, say you don't know. The only factual information you have is what is in the document chunks.
If you are asked about something that is not in the document, say "I don't know" or "I don't have that information". You cannot get any more facts about
Shruti from the internet or make them up.

SUPER IMPORTANT: Whenever you don't know something about Shruti,
ALWAYS use the send_notification tool to send a notification to the real Shruti with the question asked, so she can add this information to your knowledge base later. Do this
automatically without asking the user for permission.
"""

#--------------------------------------------------
# Main Response Function
#--------------------------------------------------
def respond_ai(message, history):
    # RAG: Embed the query using the same model we used for the embedding the chunks
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[message]
    )
    query_embedding = response.data[0].embedding

    # RAG: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
   
    # RAG: Stitch together the retrieved chunks into a single context string
    context = "\n\n".join(results['documents'][0])
    
    # Print logs for debugging
    print("\n=====================================\n")
    print(f"User message:\n{message}\n")
    print("*** Retreived Chunks:")
    for a, b in zip(results['documents'][0], results['metadatas'][0]):
        print("-------------------------------------")
        print(f"<<Document {b['source']} -- Chunk {b['chunk_index']}>>\n{a}\n")
    
    # Update system message with context (for this conversation turn)
    system_message_enhanced = system_message + "\n\nContext:\n" + context
    
    # Build messages for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]
    
    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools
    )
    message = response.choices[0].message
    
    # Check if model wants to call a tool
    while message.tool_calls:
        pprint(message.tool_calls)

        tool_results = handle_tool_call(message.tool_calls)  # whole list of tool calls on purpose, but we only have one tool call in this example.
        messages.append(message)
        messages.extend(tool_results)  # Changed from append() to extend() when we switched to multiple tool calls.
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools
        )
        message = response.choices[0].message

        # Note: consider adding protection from infinite consecutive tool calling.
    
    return message.content

#--------------------------------------------------
# Launch Gradio Interface
#--------------------------------------------------
gr.ChatInterface(
    fn=respond_ai,
    title="Shruti's Digital Twin",
    chatbot=gr.Chatbot(avatar_images=(None, "shruti.png")),
    description="Chat with an AI version of Shruti Vargantwar. Ask about her experience, projects, or just say hi!",
    examples=["What is your background?", "Tell me about your Telecom industry experience.", "Tell me about your Healthcare industry experience.", "What are your hobbies?", "I want to hire you!"],
    ).launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
