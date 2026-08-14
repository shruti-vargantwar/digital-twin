import os
from openai import OpenAI
import gradio as gr

#----------------------------------
# Setup
#----------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")
client = OpenAI()

#----------------------------------
# Document
#----------------------------------
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

#----------------------------------
# System Message
#----------------------------------
system_message = """
You are a digital twin of Shruti Vargantwar. When people talk to you, you respond AS Shruti would — in first person, using her voice, personality and knowledge.
Here is the information about Shruti Vargantwar to help you embody her:

Important: Do not make up things up. If you don't know the answer, say you don't know. The only factual information you have is what is in the document provided. If you are asked about something that is not in the document, say "I don't know" or "I don't have that information."
"""

#----------------------------------
# Main Response Function
#----------------------------------
def respond_ai(message, history):
    # Update system message with context (for this conversation turn)
    system_message_enhanced = system_message + "\n\nContext:\n" + document_overview
    
    # Logs for debugging
    print("\n=====================================\n")
    print("***User message:\n", message)
    print("\n*** Context this turn:\n", system_message_enhanced)
    
    # Build messages for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]
    
    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    message = response.choices[0].message
    
    return message.content

#----------------------------------
# Launch Gradio Interface
#----------------------------------
gr.ChatInterface(fn=respond_ai).launch(inbrowser=True)
