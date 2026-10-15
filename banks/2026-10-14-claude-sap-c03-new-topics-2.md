# SAP-C03 new-topic question bank, batch 2
source: Claude-written SAP-C03 new-topic bank (2026-10-14, unofficial)
url: banks/2026-10-14-claude-sap-c03-new-topics-2.md
version: SAP-C03 (announced topic)

40 more original scenario questions (41 to 80) written 2026-10-14 by Claude (Fable 5.1) for the owner, going one level deeper into the skill areas AWS named for SAP-C03. Not official AWS content; verify service details against the current docs. Multi-select questions say "Select TWO". Answers in the table at the end.

## Generative AI and agentic AI

41. A legal firm's assistant must always answer in the firm's house style and citation format, which the base model does not follow even with detailed prompts. The content itself comes from the firm's document store. Which combination is MOST appropriate? (Select TWO)
    A. Fine-tune a foundation model on examples of the house style to create a custom model
    B. Keep the document content in a Bedrock knowledge base and retrieve it at request time
    C. Put all documents into the fine-tuning dataset so the model memorises them
    D. Increase the temperature so the model varies its style
    E. Train a new foundation model from scratch on SageMaker

42. A product catalogue assistant must find documents by exact part numbers such as "XK-4471-B" as well as by meaning. Pure vector retrieval keeps missing the exact codes. Which knowledge base setting addresses this?
    A. Enable hybrid search (semantic plus keyword) on the knowledge base retrieval
    B. Increase the chunk size to 2,000 tokens
    C. Switch to a larger foundation model
    D. Disable embeddings and use the model's memory

43. Security testing shows that a document uploaded by a user can contain instructions that make the assistant ignore its rules and call tools it should not (prompt injection through retrieved content). Which combination reduces this risk the MOST? (Select TWO)
    A. Bedrock Guardrails with the prompt-attack filter enabled on inputs
    B. Give the agent's tool roles least-privilege permissions so a hijacked agent cannot perform damaging actions
    C. Ask the model politely in the system prompt to ignore injected instructions
    D. Store uploaded documents in a public bucket so they can be reviewed
    E. Disable CloudTrail for the agent role to reduce noise

44. An HR assistant answers questions about leave policy. The company requires that answers are provably consistent with the written policy, not just statistically likely. Which Bedrock feature is designed for this?
    A. Guardrails Automated Reasoning checks built from the policy document
    B. A higher top-p value
    C. Provisioned throughput
    D. Model distillation

45. A customer-facing chat application sends a steady 400 requests per second to one model all day and has a strict p95 latency target. On-demand invocations are being throttled at peak. Which option meets the requirement?
    A. Purchase Provisioned Throughput (model units) for the model
    B. Retry with exponential backoff only
    C. Move to batch inference
    D. Reduce the maximum tokens to zero

46. Every night a company must summarise 3 million support tickets with a foundation model. Results are needed by morning and cost is the main concern. Which approach is MOST cost-effective?
    A. Bedrock batch inference jobs reading the prompts from Amazon S3
    B. Real-time InvokeModel calls from 500 Lambda functions in parallel
    C. Provisioned Throughput reserved for the whole month
    D. A GPU EC2 fleet running an open model continuously

47. A team must choose between three foundation models for a summarisation task and justify the choice to management with measurable quality metrics, including human review of a sample. Which service feature supports this with the least custom tooling?
    A. Bedrock model evaluation jobs (automatic metrics and human-based evaluation)
    B. CloudWatch Logs Insights queries over invocation logs
    C. AWS Trusted Advisor
    D. A spreadsheet of opinions from the team

48. Auditors require a record of every prompt and response sent to Bedrock across all applications in the account, delivered centrally, with sensitive values masked before storage. Which solution meets this?
    A. Enable Bedrock model invocation logging to CloudWatch Logs or S3 and apply a CloudWatch Logs data-protection policy to mask sensitive data
    B. Ask each application team to print prompts to stdout
    C. Enable VPC Flow Logs on the application subnets
    D. Enable AWS Config on the Bedrock service

49. An agent must run Python code that the model generates to analyse uploaded spreadsheets, and the code must execute in an isolated sandbox that cannot reach the company network. Which AgentCore capability fits?
    A. AgentCore Code Interpreter
    B. Running the code on the agent's own EC2 host
    C. AgentCore Memory
    D. AWS Lambda with a VPC configuration and internet access

50. An organisation wants to require that every application in the organisation invokes Bedrock models only with an approved guardrail attached. Which mechanism enforces this at the IAM layer?
    A. An IAM or SCP condition on bedrock:InvokeModel using the bedrock:GuardrailIdentifier condition key to require the approved guardrail
    B. A CloudWatch alarm on invocation count
    C. Tagging the models
    D. A Lambda function that reviews CloudTrail weekly

## Resilience engineering

51. After every production deployment, the architecture team wants the resilience assessment re-run automatically and the deployment marked failed if the application no longer meets its RTO and RPO policy. Which design meets this?
    A. Call the AWS Resilience Hub assessment API from the pipeline after deployment and fail the stage when the assessment result does not meet the policy
    B. Run a manual game-day each quarter
    C. Add more Availability Zones to the VPC
    D. Enable Trusted Advisor notifications

52. A team wants to test that an EKS workload tolerates pod terminations and node failures using AWS-managed fault injection rather than custom scripts. Which option is correct?
    A. AWS Fault Injection Service actions for EKS (pod and node faults) in an experiment template with a stop-condition alarm
    B. Deleting nodes manually from the console
    C. AWS Config conformance packs
    D. A Lambda cron that reboots random instances

53. A two-Region application failed over successfully in a test but could not scale in the recovery Region because EC2 quotas there were lower. The team wants such mismatches detected continuously before an incident. Which feature provides this?
    A. Route 53 ARC readiness checks, which compare resource configuration and quotas across the application's Regions
    B. AWS Budgets
    C. Amazon Inspector
    D. EC2 Auto Scaling warm pools

54. A company enabled zonal autoshift for its load balancers but wants assurance, every week, that the application actually runs correctly on only two of its three Availability Zones. Which feature provides this?
    A. Zonal autoshift practice runs that shift traffic away from one AZ on a schedule, with alarms that stop the practice if the application degrades
    B. A longer health-check interval
    C. Enabling cross-zone load balancing
    D. Deleting one subnet from the VPC

55. Incidents currently depend on an on-call engineer finding the right runbook in a wiki. The company wants automated engagement of responders, a tracked timeline, and runbooks that run automatically when an alarm fires. Which service should the architect use?
    A. AWS Systems Manager Incident Manager with response plans, escalation and automation runbooks
    B. Amazon SNS email only
    C. AWS Health Dashboard
    D. Amazon Connect

## Cloud-native patterns

56. A Lambda function processes payment messages from SQS. Because of retries, the same message occasionally invokes the function twice and charges the customer twice. Which change is MOST appropriate?
    A. Make the function idempotent by storing a processed-message key in DynamoDB with a conditional write (for example with Powertools for AWS Lambda idempotency)
    B. Lower the SQS visibility timeout
    C. Increase the Lambda memory size
    D. Switch to a standard queue with long polling

57. Records from a Kinesis data stream must be filtered, enriched by a Lambda function and then passed to Step Functions, with no polling code to maintain. Which service provides this?
    A. Amazon EventBridge Pipes with a Kinesis source, filter, enrichment and Step Functions target
    B. An EC2 consumer application
    C. AWS Glue streaming jobs
    D. Amazon MQ

58. A nightly job must process 4 million objects in an S3 bucket, with each object handled independently and the whole run finished in under an hour. Which Step Functions feature fits?
    A. A Distributed Map state that iterates the S3 object list and runs child workflows in parallel at high concurrency
    B. A single Lambda function with a for loop
    C. An inline Map state with a maximum concurrency of 40
    D. A Wait state

59. A SaaS provider offers a premium tier with dedicated resources and compliance isolation, and a standard tier that shares resources. Tenants must be routed to the right tier automatically. Which design is MOST appropriate?
    A. A siloed deployment per premium tenant and a pooled deployment for standard tenants, with tenant-aware routing (for example by tenant identity in the JWT) at the API layer
    B. One deployment for all tenants with a flag in the database
    C. A separate AWS Region per tenant
    D. Hard-coded URLs per tenant in the client

60. Security wants containers on EKS to run with the least possible privilege: no root, read-only file systems, immutable image tags, and pods that obtain AWS credentials without using the node's instance role. Which combination meets this? (Select TWO)
    A. Pod security standards (restricted profile) enforced by an admission policy, with ECR tag immutability enabled
    B. EKS Pod Identity (or IAM roles for service accounts) so each pod gets its own IAM role
    C. Running pods as privileged to simplify debugging
    D. Attaching AdministratorAccess to the node instance role
    E. Using the latest tag for all images

61. An application relies on Apache Kafka client libraries and exactly-once semantics, and the team does not want to manage brokers or capacity. Which service should be used?
    A. Amazon MSK Serverless
    B. Amazon Kinesis Data Streams
    C. Amazon SQS FIFO
    D. Self-managed Kafka on EC2

62. A company runs a service on ECS and is migrating it to EKS. During the migration, callers across several VPCs must reach a single service name while traffic is shifted gradually from ECS to EKS by weight. Which service enables this?
    A. Amazon VPC Lattice with a service that has weighted target groups for the ECS and EKS backends
    B. A static DNS entry per cluster
    C. Classic Load Balancer with sticky sessions
    D. VPC peering plus manual route edits

## DevSecOps and observability

63. The platform team wants to reject infrastructure code that opens security groups to the internet or creates unencrypted volumes before anything is deployed, as policy-as-code in the pipeline. Which approach fits?
    A. Run AWS CloudFormation Guard (cfn-guard) rules, or cdk-nag for CDK, in the build stage and fail on violations
    B. Review templates by email
    C. Rely on AWS Config to flag resources after deployment only
    D. Give developers a checklist

64. A Lambda-based API must be released to production with gradual traffic shifting and automatic rollback if the error rate rises. Which solution is correct?
    A. AWS CodeDeploy canary or linear deployment on a Lambda alias with CloudWatch alarms configured for rollback
    B. Replace the function code in place with the console
    C. A Route 53 weighted record between two accounts
    D. Deploy on Friday evening with a manual check

65. A company uses GitHub Actions to deploy to AWS. Security requires no long-lived AWS access keys in GitHub and all deploy-time secrets to be rotated automatically. Which combination meets this? (Select TWO)
    A. GitHub OpenID Connect federation with an IAM role trust policy restricted to the repository and branch
    B. AWS Secrets Manager with automatic rotation for the application secrets referenced at deploy time
    C. An IAM user access key stored as a GitHub secret and rotated yearly
    D. Secrets committed to the repository in an encrypted zip
    E. The root user's credentials in an environment variable

66. A microservice platform on EKS needs distributed traces, metrics and application-level SLO tracking with OpenTelemetry-compatible collection. Which combination is MOST appropriate? (Select TWO)
    A. The AWS Distro for OpenTelemetry (ADOT) collector exporting traces to AWS X-Ray and metrics to Amazon Managed Service for Prometheus
    B. CloudWatch Application Signals enabled for the EKS cluster
    C. VPC Reachability Analyzer
    D. S3 server access logs
    E. AWS Shield Advanced

67. Users of a Bedrock application report occasional slow or failed responses. The operations team needs dashboards and alarms for model invocation latency, errors and throttling per model without instrumenting the application. Which solution meets this?
    A. CloudWatch metrics published by Amazon Bedrock in the AWS/Bedrock namespace (invocations, latency, errors, throttles) with dashboards and alarms
    B. Enabling GuardDuty on the account
    C. Running a load test every hour
    D. Reading CloudTrail events by hand

68. Finance wants to be alerted to unusual spend patterns in any account and to automatically stop a sandbox account's EC2 instances when its monthly budget is exceeded. Which combination meets this? (Select TWO)
    A. AWS Cost Anomaly Detection monitors with alert subscriptions
    B. AWS Budgets with a budget action that applies a deny policy or stops the instances when the threshold is crossed
    C. Cost Explorer reports reviewed quarterly
    D. Deleting the sandbox account
    E. Reserved Instances for the sandbox

## Data and analytics

69. A data team stores Iceberg tables in S3 but spends significant effort on compaction, snapshot expiry and small-file cleanup. They want AWS to manage this maintenance automatically. Which option should they choose?
    A. Amazon S3 Tables, which provide managed Apache Iceberg tables with automatic maintenance
    B. Converting the tables to CSV
    C. Running compaction from a cron job on EC2
    D. Moving the data to EBS volumes

70. Bad records (null keys, out-of-range values) keep reaching the curated zone of a data lake. The team wants rules evaluated inside the ETL pipeline and the load to stop when data quality falls below a threshold. Which feature fits?
    A. AWS Glue Data Quality rules evaluated in the Glue job or pipeline, with a failure action when the score falls below the threshold
    B. Amazon Macie
    C. Amazon Athena federated queries
    D. S3 Object Lock

71. Analysts need near-real-time reporting on transactional data in Amazon Aurora, and the team wants to avoid building and operating an ETL pipeline. Which solution is MOST appropriate?
    A. Aurora zero-ETL integration with Amazon Redshift
    B. A nightly DMS full load into Redshift
    C. Querying the production Aurora writer directly from the BI tool
    D. Exporting CSVs to S3 by hand

72. A data lake has 500 tables and permissions are granted table by table, which has become unmanageable. Some tables also need row-level restrictions by country. Which combination addresses both needs? (Select TWO)
    A. Lake Formation tag-based access control (LF-tags) so permissions follow tags rather than individual tables
    B. Lake Formation data filters for row-level and cell-level security
    C. S3 bucket policies per analyst
    D. A copy of each table per country
    E. IAM inline policies on every user

## Post-quantum cryptography

73. A company signs software artefacts with an ECDSA key in KMS and wants to move to a post-quantum algorithm without breaking consumers who still verify with the old key. Which approach is MOST appropriate?
    A. Introduce an ML-DSA KMS key and dual-sign artefacts during a transition period while consumers add support for verifying ML-DSA signatures, then retire the ECDSA key
    B. Delete the ECDSA key immediately
    C. Increase the ECDSA curve to P-521
    D. Stop signing artefacts

74. Management wants the organisation to be "crypto-agile": able to change algorithms later with minimal application change. Which practice best supports this on AWS?
    A. Centralise cryptographic operations in AWS KMS (and managed services that use it) so key specs and algorithms can change without rewriting application code, and inventory algorithm use with CloudTrail and Config
    B. Implement custom cryptography in each application
    C. Hard-code the algorithm name in every service
    D. Use one shared static key for all systems

75. A security review classifies workloads for post-quantum migration priority. Which items should be migrated FIRST?
    A. Long-lived digital signatures and data in transit that could be recorded now and decrypted later
    B. AES-256 encrypted data at rest, which quantum computers break immediately
    C. SHA-256 checksums of log files
    D. Nothing, because symmetric encryption is affected first

## Cross-domain SAP-C03 scenarios

76. A GenAI application must keep serving if its primary Region fails. The knowledge base is built from documents in S3 and the application uses on-demand inference. Which combination gives Regional resilience with the least operational effort? (Select TWO)
    A. Replicate the source documents with S3 Cross-Region Replication and maintain a knowledge base in the second Region that syncs from the replica
    B. Use cross-Region inference profiles so model invocations can be served from more than one Region
    C. Copy the vector index by hand after each change
    D. Run the model on EC2 in both Regions
    E. Point the application to a single Region and accept the outage

77. An AI agent handles bursty, infrequent workloads: a few hundred sessions per day with long idle periods. The team wants to pay only while sessions run and not operate servers. Which hosting option fits?
    A. Amazon Bedrock AgentCore Runtime, which bills for consumed resources per session
    B. A fleet of always-on EC2 instances
    C. A dedicated EKS cluster
    D. Provisioned Throughput reserved for a year

78. A regulated company must prove to auditors which teams used which foundation models, in which Regions, and that every invocation went through an approved guardrail. Which combination provides this evidence? (Select TWO)
    A. CloudTrail data events for Bedrock invocations, organisation-wide, delivered to a central log archive
    B. Application inference profiles with cost-allocation tags plus IAM conditions that require the approved guardrail
    C. Screenshots of the console taken monthly
    D. Trusted Advisor checks
    E. Disabling model invocation logging to reduce storage

79. A Java monolith on EC2 must be moved to containers with the least manual Dockerfile authoring and then deployed on ECS with a CI/CD pipeline. Which approach is MOST appropriate?
    A. AWS App2Container to discover the application, generate the container image and deployment artefacts, then deploy to ECS through the generated pipeline
    B. Rewrite the application as Lambda functions first
    C. Run the JAR directly on Fargate without a container image
    D. Keep the EC2 instance and add an Auto Scaling group

80. During incidents, engineers spend most of their time correlating alarms, logs and recent changes across services. The company wants AI-assisted triage inside its observability tooling with suggested hypotheses and runbooks. Which capability addresses this?
    A. CloudWatch investigations (operational investigations assisted by Amazon Q Developer) that correlate metrics, logs and deployment changes
    B. Increasing the number of CloudWatch dashboards
    C. Exporting all logs to a spreadsheet
    D. Disabling alarms during incidents

## Answers

| # | Answer | Why |
| --- | --- | --- |
| 41 | A,B | Style and format are learned behaviour, which fine-tuning captures; the facts stay in a knowledge base so they can change without retraining. Memorising documents by fine-tuning goes stale; temperature does not fix style; training from scratch is impractical |
| 42 | A | Hybrid search combines semantic similarity with keyword matching so exact identifiers are found. Larger chunks, bigger models and dropping embeddings do not solve exact-match retrieval |
| 43 | A,B | The prompt-attack filter detects injection attempts in inputs; least-privilege tool roles limit the blast radius if an attack succeeds. Polite prompts are not a control; public buckets and disabled logging make things worse |
| 44 | A | Automated Reasoning checks validate responses against formal rules derived from the policy, giving verifiable rather than probabilistic consistency. Sampling parameters, throughput and distillation do not add verification |
| 45 | A | Provisioned Throughput reserves model units for consistent, high-volume, latency-sensitive traffic. Backoff alone still throttles; batch inference is asynchronous; zero tokens produces no output |
| 46 | A | Batch inference processes large offline workloads from S3 at a lower price than on-demand. Parallel real-time calls cost more; provisioned capacity for a nightly job sits idle; a GPU fleet adds operations and cost |
| 47 | A | Bedrock model evaluation jobs run automatic metrics and human evaluation workflows with reports. Log queries, Trusted Advisor and opinions do not give measurable quality comparisons |
| 48 | A | Model invocation logging captures prompts and responses centrally; a Logs data-protection policy masks sensitive data at ingestion. stdout, flow logs and Config do not capture prompt content |
| 49 | A | AgentCore Code Interpreter runs model-generated code in an isolated sandbox. The agent host, Memory and an internet-connected Lambda do not give the required isolation |
| 50 | A | The bedrock:GuardrailIdentifier condition key lets IAM and SCPs require a specific guardrail on invocations. Alarms, tags and weekly reviews detect rather than enforce |
| 51 | A | Resilience Hub exposes assessment APIs that pipelines can call to gate deployments on the resiliency policy. Quarterly game-days, extra AZs and Trusted Advisor do not give per-deployment gating |
| 52 | A | FIS has native EKS actions (pod deletion, CPU and memory stress, node faults) with stop conditions. Manual deletion, Config and random reboots lack control and safety |
| 53 | A | ARC readiness checks continuously compare configuration, capacity and quotas between the application's Regions and flag mismatches. Budgets, Inspector and warm pools are unrelated |
| 54 | A | Zonal autoshift practice runs regularly shift traffic away from an AZ to prove the application copes, and stop if alarms fire. Health-check intervals, cross-zone balancing and deleting subnets do not test this |
| 55 | A | Incident Manager provides response plans, contact escalation, timelines and runbook automation triggered by alarms. SNS email, the Health Dashboard and Connect do not manage incidents |
| 56 | A | Idempotency with a conditional write records each processed message so a duplicate delivery is a no-op; this is the standard pattern for at-least-once sources. Visibility timeout, memory and queue type do not remove duplicates |
| 57 | A | EventBridge Pipes connects a source to a target with filtering and enrichment steps, with no polling code. EC2 consumers, Glue streaming and MQ require code or do not fit the flow |
| 58 | A | Distributed Map processes large datasets, including S3 listings, with thousands of parallel child executions. A single function, an inline Map (limited concurrency) and a Wait state cannot finish in time |
| 59 | A | Tiered isolation (silo for premium, pool for standard) with tenant-aware routing is the SaaS reference pattern. A database flag gives no isolation; a Region per tenant and hard-coded URLs do not scale |
| 60 | A,B | The restricted Pod Security Standard enforced by an admission policy gives no root and read-only file systems, and immutable tags prevent image swaps; Pod Identity or IRSA gives each pod its own role. Privileged pods, admin node roles and latest tags are the opposite |
| 61 | A | MSK Serverless gives Kafka API compatibility with no broker or capacity management. Kinesis and SQS FIFO are not Kafka; self-managed Kafka means operating brokers |
| 62 | A | VPC Lattice services support weighted target groups across compute types, so one name can shift traffic between ECS and EKS. Static DNS, sticky CLBs and manual routes do not provide weighted migration |
| 63 | A | cfn-guard and cdk-nag evaluate templates against rules before deployment and fail the build. Email review, post-deployment Config and checklists are not preventive gates |
| 64 | A | CodeDeploy traffic-shifting deployments for Lambda aliases shift gradually and roll back automatically on alarm. In-place replacement, DNS weighting across accounts and manual checks lack automatic rollback |
| 65 | A,B | OIDC federation removes stored AWS keys and scopes the role to the repository; Secrets Manager rotation handles the application secrets. Stored keys, committed secrets and root credentials violate the requirement |
| 66 | A,B | ADOT is the OpenTelemetry-based collector feeding X-Ray and Managed Prometheus; Application Signals adds SLOs for EKS services. Reachability Analyzer, S3 logs and Shield are unrelated |
| 67 | A | Bedrock publishes per-model invocation, latency, error and throttling metrics automatically. GuardDuty, load tests and CloudTrail reading are not operational dashboards |
| 68 | A,B | Cost Anomaly Detection flags unusual spend with alerts; Budgets actions can apply a deny policy or stop instances when a threshold is crossed. Quarterly reviews, deleting the account and RIs do not meet the requirements |
| 69 | A | S3 Tables are fully managed Iceberg tables with automatic compaction, snapshot management and cleanup. CSV, cron compaction and EBS all remove or keep the burden |
| 70 | A | Glue Data Quality evaluates rules inside the pipeline and can fail the job below a threshold. Macie, Athena federation and Object Lock are not data-quality controls |
| 71 | A | Zero-ETL integration replicates Aurora data into Redshift continuously with no pipeline. Nightly loads are not near real time; querying the writer harms production; manual exports are not a solution |
| 72 | A,B | LF-tags scale permissions by attribute instead of per table; data filters provide row- and cell-level security. Bucket policies, table copies and inline policies do not scale |
| 73 | A | Dual signing with a new ML-DSA key preserves compatibility while consumers migrate, which is the crypto-agility pattern. Deleting the key breaks consumers; a larger curve is still quantum-vulnerable; not signing removes integrity |
| 74 | A | Centralising in KMS means an algorithm or key-spec change does not require application rewrites, and CloudTrail and Config give an inventory. Custom crypto, hard-coded algorithms and shared static keys reduce agility and security |
| 75 | A | Public-key signatures and recorded TLS traffic are exposed to harvest-now-decrypt-later and Shor's algorithm; symmetric AES-256 and SHA-256 remain adequate under Grover's algorithm with current key sizes |
| 76 | A,B | CRR plus a second knowledge base keeps retrieval available; cross-Region inference profiles keep model invocations available. Manual index copies, self-hosted models and accepting the outage do not meet the goal |
| 77 | A | AgentCore Runtime is serverless and bills for consumption per session, suiting bursty traffic. Always-on EC2, a dedicated EKS cluster and year-long Provisioned Throughput pay for idle time |
| 78 | A,B | CloudTrail data events give the who, what and where of invocations; inference profiles tag usage to teams and the guardrail condition proves enforcement. Screenshots, Trusted Advisor and disabling logs do not provide evidence |
| 79 | A | App2Container analyses the running Java application, builds the image and generates ECS deployment and pipeline artefacts. Rewriting as Lambda, running a bare JAR and keeping EC2 do not meet the containerisation goal |
| 80 | A | CloudWatch investigations use Amazon Q Developer to correlate telemetry and changes and suggest hypotheses and remediation. More dashboards, spreadsheets and disabled alarms do not help triage |
