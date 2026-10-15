# SAP-C03 new-topic question bank
source: Claude-written SAP-C03 new-topic bank (2026-10-14, unofficial)
url: banks/2026-10-14-claude-sap-c03-new-topics-1.md
version: SAP-C03 (announced topic)

40 original scenario questions written 2026-10-14 by Claude (Fable 5.1) for the owner, covering every new skill area AWS named for SAP-C03 in its 1 September 2026 announcement. Not official AWS content; verify any service detail against the current docs before exam day. Multi-select questions say "Select TWO". Answers in the table at the end.

## Generative AI and agentic AI

1. A company wants a customer-support assistant on Amazon Bedrock that answers from 40,000 internal PDF manuals in Amazon S3. The manuals change weekly and the model must never be retrained. Which design meets these requirements with the LEAST operational overhead?
   A. Fine-tune a foundation model on the manuals every week with a custom model job
   B. Create a Bedrock knowledge base with the S3 bucket as the data source and a managed vector store, and sync it on a weekly schedule
   C. Load every manual into the prompt context on each request
   D. Train a custom embedding model on SageMaker and store vectors in an EC2-hosted database

2. A healthcare application calls Amazon Bedrock. Regulators require that the model never discusses competitor drug pricing and that patient identifiers in responses are masked. The prompt is written by many development teams. Which solution enforces this consistently?
   A. Add an instruction to every team's system prompt asking the model to avoid the topics
   B. Create a Bedrock guardrail with a denied topic and a sensitive-information filter set to mask PII, and attach it to every model invocation and agent
   C. Run a regular expression over responses in each application
   D. Use a smaller model that has less knowledge of pricing

3. A RAG application sometimes answers with facts that are not in the retrieved documents. The company wants such responses blocked before they reach users, without changing the model. Which feature should the solutions architect use?
   A. Bedrock Guardrails contextual grounding check
   B. A higher temperature setting
   C. Amazon Comprehend sentiment analysis
   D. Provisioned throughput for the model

4. A company is building an AI agent that reads order status from an internal REST API and can issue refunds through an existing Lambda function. The agent must run as a managed, isolated session per user and the tools must be exposed over the Model Context Protocol without rewriting the API. Which combination of services fits? (Select TWO)
   A. Amazon Bedrock AgentCore Runtime to host the agent with per-session isolation
   B. Amazon Bedrock AgentCore Gateway to expose the REST API and the Lambda function as MCP tools
   C. An Auto Scaling group of EC2 instances running the agent framework
   D. Amazon API Gateway WebSocket APIs to host the model
   E. AWS Batch to run each agent session as a job

5. An agent must call a third-party SaaS API on behalf of the signed-in user using that user's own OAuth consent. Developers must not embed shared service credentials in the agent. Which service provides this capability?
   A. AWS Secrets Manager with a single shared API key
   B. Amazon Bedrock AgentCore Identity with outbound OAuth 2.0 authorization and a token vault
   C. IAM user access keys rotated monthly
   D. Amazon Cognito identity pools with unauthenticated access

6. An agent drafts fee reversals. Reversals above 200 USD must be approved by a human before any money moves, and the approval may take hours. Which design is MOST appropriate?
   A. Let the agent call the ledger API directly and log every call to CloudTrail
   B. Orchestrate the reversal in AWS Step Functions with a waitForTaskToken callback task; a human approves in a ticketing tool, which sends the task token back, and only then is the ledger Lambda invoked
   C. Pause the Lambda function with a sleep until the approver replies
   D. Put the approval in the prompt and trust the model to wait

7. A travel-booking agent must remember a traveller's seat preferences across conversations that happen weeks apart, while keeping each conversation's working context separate. Which AgentCore capability provides this?
   A. AgentCore Memory with short-term session memory and long-term memory strategies
   B. Storing the entire chat history in the system prompt
   C. Amazon ElastiCache with a 1-hour TTL
   D. Bedrock model fine-tuning on each customer's history

8. A financial firm requires that all traffic between its VPC applications and Amazon Bedrock stays on the AWS network, and that only approved foundation models in approved Regions can be invoked anywhere in the organization. Which combination meets these requirements? (Select TWO)
   A. VPC interface endpoints (AWS PrivateLink) for the Bedrock runtime endpoints, with an endpoint policy
   B. A NAT gateway with a static IP allow-listed by AWS
   C. A service control policy that denies bedrock:InvokeModel unless the model ARN and Region match the approved list
   D. A security group rule that allows 0.0.0.0/0 on port 443
   E. Amazon Macie scanning of the prompts

9. A company runs several Bedrock applications for different business units in one account and needs to charge each unit for its own token usage, and to spread on-demand traffic across Regions to avoid throttling. Which combination should the architect use? (Select TWO)
   A. Application inference profiles tagged per business unit
   B. A separate AWS account for every prompt
   C. Cross-Region inference profiles for the invocations
   D. Reserved Instances for Bedrock
   E. Amazon Athena queries over CloudTrail to estimate cost

10. A SaaS vendor serves 300 tenants from one Bedrock knowledge base. A tenant must never retrieve another tenant's documents. Which approach enforces this at retrieval time with the least duplication?
    A. One knowledge base per tenant, each with its own vector store
    B. Tag each document with tenant metadata and apply a metadata filter on every Retrieve call from a tenant-scoped IAM role
    C. Ask the model in the prompt to ignore other tenants' documents
    D. Encrypt each tenant's documents with a different KMS key in the same index

11. The operations team needs traces of each agent run, including tool calls, latencies and token counts, and alarms when guardrails intervene more than 5% of the time. Which solution meets this with the least custom code?
    A. AgentCore Observability with OpenTelemetry traces into CloudWatch, plus CloudWatch alarms on Bedrock guardrail-intervention and invocation metrics
    B. A custom logging library that writes every prompt to Amazon S3
    C. AWS Config rules on the agent's IAM role
    D. VPC Flow Logs on the agent's subnet

## Resilience engineering

12. A company has an RTO of 30 minutes and an RPO of 5 minutes for a three-tier application. Management wants an evidence-based report showing whether the current architecture meets these targets and what to change. Which service provides this?
    A. AWS Trusted Advisor
    B. AWS Resilience Hub with a resiliency policy that defines the RTO and RPO, and an application assessment
    C. AWS Well-Architected Tool lens review only
    D. Amazon DevOps Guru

13. Before a peak event, the team wants to prove that the application survives the loss of one Availability Zone, but any experiment must stop automatically if the customer error rate rises above 2%. Which solution is correct?
    A. Terminate instances by hand in one AZ during a change window
    B. An AWS Fault Injection Service experiment using the AZ availability scenario, with a CloudWatch alarm on the error rate configured as a stop condition
    C. Run a load test with Distributed Load Testing on AWS
    D. Disable the AZ in the Auto Scaling group permanently

14. During an incident, the application's health checks pass but customers in one Availability Zone see timeouts (a gray failure). The team needs a way to move traffic away from the impaired AZ in minutes without redeploying. Which feature should be in the design?
    A. Amazon Route 53 Application Recovery Controller zonal shift (and zonal autoshift) for the load balancer
    B. A larger instance type in every AZ
    C. Route 53 weighted records pointing to each instance
    D. A longer DNS TTL

15. A payment platform runs active-standby across two Regions. Failover must be triggered deliberately by an operator, must not depend on the primary Region's control plane, and readiness of the standby must be checked continuously. Which solution meets these requirements?
    A. Route 53 ARC routing controls in a highly available cluster with readiness checks, operated from the standby Region
    B. A Lambda function in the primary Region that updates Route 53 records
    C. CloudFront origin failover only
    D. Manual edits to the Route 53 hosted zone during the incident

16. When a CloudWatch alarm detects a filling disk on a fleet of EC2 instances, the company wants an automated, auditable remediation that expands the volume and the file system, with no engineer logged in. Which solution should the architect propose?
    A. An EventBridge rule on the alarm state change that starts an AWS Systems Manager Automation runbook which modifies the EBS volume and runs the resize commands through Run Command
    B. A cron job on each instance with sudo
    C. An SSH bastion that engineers use during the alarm
    D. Replacing the instance from the AMI on every alarm

## Cloud-native patterns

17. Files land in Amazon S3 at random times. Each file must be validated, transformed and loaded into a data lake within 15 minutes, with retries and a clear record of each failed file. The team wants to run no servers. Which design is MOST appropriate?
    A. An EC2 instance that polls the bucket every minute
    B. S3 event notifications to Amazon EventBridge, which starts an AWS Step Functions workflow that runs Lambda validation and an AWS Glue job, with retry and catch states and failed inputs sent to an SQS dead-letter queue
    C. A nightly batch on Amazon EMR
    D. A Kinesis Data Streams consumer on Fargate running 24/7

18. An order workflow has 12 steps, waits up to 3 days for a supplier callback, and must retry transient failures with exponential backoff while guaranteeing each step runs at most once. Which choice is correct?
    A. AWS Step Functions Standard workflow with Retry fields and a callback task with a task token
    B. AWS Step Functions Express workflow
    C. A chain of SQS queues with Lambda consumers and no state store
    D. An Amazon MQ broker with manual compensation

19. Fifty microservices run across ECS, EKS and Lambda in 12 accounts. Teams need service-to-service HTTP calls across accounts with IAM-based authorization on every request and no sidecar to manage. Which service should be used?
    A. AWS App Mesh
    B. Amazon VPC Lattice with a shared service network and auth policies
    C. VPC peering between every pair of VPCs
    D. An internet-facing ALB per service with API keys

20. A team runs all its microservices on Amazon ECS in one cluster. They want service discovery by name, per-service traffic metrics and retries in ECS without operating a service mesh control plane. Which feature should they enable?
    A. Amazon ECS Service Connect
    B. AWS App Mesh with a self-managed Envoy control plane
    C. Classic Load Balancers
    D. Static IP addresses in task definitions

21. The security team requires that container images with critical CVEs never reach the production EKS cluster, that images are continuously rescanned as new CVEs are published, and that only images built by the pipeline can run. Which combination meets these requirements? (Select TWO)
    A. Amazon ECR enhanced scanning (Amazon Inspector) with a pipeline stage that fails the deployment on critical findings
    B. Scanning images once on the developer laptop
    C. Signing images in the pipeline with AWS Signer and enforcing signature verification with an admission controller in EKS
    D. Running all containers as root to simplify patching
    E. Disabling image tag immutability

22. A SaaS provider is designing a pooled multi-tenant backend on DynamoDB and Lambda. A tenant must only ever read its own items, enforced by IAM rather than application code, with one Lambda function for all tenants. Which design is correct?
    A. A tenant identifier as the partition key prefix and an IAM policy with a dynamodb:LeadingKeys condition on session tags set at AssumeRole time (ABAC)
    B. One DynamoDB table per tenant and one Lambda function per tenant
    C. A WHERE clause in the application that filters by tenant
    D. A single admin role shared by every tenant

23. A ride-hailing company must compute driver-surge pricing within 2 seconds of location events from 2 million vehicles, and also keep every event for daily batch reporting. Which design meets both needs?
    A. Amazon Kinesis Data Streams with Amazon Managed Service for Apache Flink for the real-time computation, and Amazon Data Firehose delivering the same stream to Amazon S3 in Iceberg format for batch analytics
    B. Write every event to Amazon RDS and run a query every second
    C. Amazon SQS FIFO with one consumer
    D. Daily AWS Glue jobs only

## DevSecOps and observability

24. A company wants every build to fail if the application's dependencies or the resulting container image contain a critical vulnerability, with the results visible centrally. The pipeline runs on AWS CodeBuild. Which solution is MOST appropriate?
    A. Amazon Inspector CI/CD integration (SBOM generation and scan in the CodeBuild stage) that fails the build on critical findings and sends results to Security Hub
    B. A weekly manual review of package.json
    C. GuardDuty runtime monitoring only
    D. Amazon Macie scanning the source bucket

25. An organization has 60 workload accounts. A central platform team must deploy infrastructure to all of them from one pipeline with no long-lived credentials, and the pipeline must not have administrator rights in the management account. Which design is correct?
    A. Run the pipeline in the management account with AdministratorAccess
    B. Run the pipeline in a dedicated tooling account; it assumes a least-privilege deployment role in each target account (for example with AWS CDK Pipelines or CloudFormation StackSets with service-managed permissions)
    C. Store an access key for each account in the pipeline's environment variables
    D. Give every developer the root credentials of each account

26. A platform team runs 40 EKS clusters and needs per-container CPU, memory, network and control-plane metrics with dashboards and alarms, using managed services and open standards. Which combination fits? (Select TWO)
    A. CloudWatch Container Insights with enhanced observability for EKS
    B. A cron job that runs kubectl top and emails the output
    C. Amazon Managed Service for Prometheus with Amazon Managed Grafana
    D. VPC Flow Logs only
    E. AWS Config aggregator

27. A company runs a Bedrock-based assistant and a SageMaker fraud model. They need alarms on model latency and token spend, and detection of data drift in the fraud model's inputs over time. Which combination should be used? (Select TWO)
    A. CloudWatch metrics for Bedrock (invocation latency, input and output token counts) with alarms and a billing budget
    B. Amazon SageMaker Model Monitor with a data-quality baseline and scheduled monitoring jobs
    C. VPC Reachability Analyzer
    D. AWS Trusted Advisor checks
    E. Amazon Inspector

28. Users report that checkout is slow, but server-side metrics look healthy. The team wants to measure real browser performance by page and region, and to be paged when a scripted checkout flow fails even when no users are active. Which solution should the architect recommend?
    A. CloudWatch RUM for real-user page performance plus CloudWatch Synthetics canaries that run the checkout flow on a schedule
    B. ALB access logs analysed weekly
    C. A larger ALB
    D. Route 53 health checks on the home page only

29. A company wants service-level objectives such as "99.9% of API calls under 300 ms" tracked automatically across its microservices, with burn-rate alarms, and minimal instrumentation work. Which feature meets this?
    A. CloudWatch Application Signals with SLOs
    B. Custom metrics written from every function by hand
    C. S3 access logs
    D. Trusted Advisor

## Data and analytics

30. A data platform must support ACID updates and deletes on petabyte-scale tables in Amazon S3, schema evolution, time travel, and queries from Athena, EMR and Redshift, with fine-grained column-level permissions managed centrally. Which design is MOST appropriate?
    A. Apache Iceberg tables on Amazon S3 registered in the AWS Glue Data Catalog, with AWS Lake Formation permissions (including LF-tags) governing access
    B. CSV files in S3 with bucket policies per team
    C. One Redshift cluster that copies all data every night
    D. An EBS-backed Hadoop cluster

31. A central data account must share specific Lake Formation tables with 25 consumer accounts, so that each sees only permitted columns, without copying the data. Which approach is correct?
    A. Replicate the S3 bucket to every consumer account
    B. Lake Formation cross-account grants (delivered through AWS Resource Access Manager) on the tables and columns, which consumers link into their own catalog
    C. Make the S3 bucket public with a prefix per consumer
    D. Export the tables to CSV monthly and email them

32. Two retailers want to measure the overlap of their customer bases and joint campaign lift. Neither is allowed to see the other's raw customer records. Which service enables this?
    A. AWS Clean Rooms with analysis rules that permit only aggregate queries on the joined data (optionally with differential privacy)
    B. A shared S3 bucket with both datasets
    C. Cross-account Aurora read replicas
    D. AWS DataSync between the two accounts

33. Clickstream events must be queryable within one minute of arrival and also kept in the same lakehouse table for historical analysis, with no duplicate ingestion pipelines. Which solution meets this?
    A. Amazon Data Firehose delivering the stream directly into an Apache Iceberg table in S3 (or S3 Tables), queried by Athena for both near-real-time and historical analysis
    B. Writing events to DynamoDB and exporting weekly
    C. Separate Kinesis and EMR pipelines writing to different buckets
    D. Streaming into Amazon RDS

## Post-quantum cryptography

34. A software vendor signs firmware that devices will verify for 15 or more years. The security team wants signatures that remain secure against a future cryptographically relevant quantum computer, using a managed key. Which choice is correct?
    A. An AWS KMS asymmetric key with an ML-DSA key spec (for example ML_DSA_65) used for sign and verify
    B. A 4096-bit RSA key in KMS
    C. An ECDSA P-256 key in KMS
    D. SSE-S3 encryption on the firmware bucket

35. A bank is worried that TLS sessions to AWS KMS and Secrets Manager recorded today could be decrypted later by a quantum computer (harvest-now, decrypt-later). Which measure addresses this?
    A. Use hybrid post-quantum TLS with ML-KEM key establishment on the KMS and Secrets Manager endpoints through an SDK that supports it (for example the AWS Common Runtime)
    B. Increase the TLS session timeout
    C. Switch to HTTP inside the VPC
    D. Rotate the KMS keys daily

36. In the context of AWS KMS post-quantum support, which statement correctly distinguishes the two algorithm families?
    A. ML-KEM is used for key encapsulation and establishment; ML-DSA is used for digital signatures
    B. ML-DSA is used for symmetric encryption; ML-KEM is used for hashing
    C. Both replace AES for data-at-rest encryption
    D. ML-KEM is a signature scheme and ML-DSA is a key exchange

## Cross-domain SAP-C03 scenarios

37. A bank wants a customer-service agent that can read account notes and draft fee reversals. Reversals over 200 USD need human approval, account numbers must never appear in logs, and the model must refuse account-takeover questions. Which combination is the MOST secure and operationally simple? (Select TWO)
    A. A Bedrock agent with a knowledge base scoped by IAM, a guardrail that denies the account-takeover topic and masks account numbers, and an approval step implemented with Step Functions before the reversal tool runs
    B. A single administrator IAM user whose keys the agent uses for all tools
    C. CloudWatch Logs data-protection policies (or redaction in the application) so account numbers are masked before logs are written
    D. Prompts stored in a public S3 bucket for easier debugging
    E. The agent writing directly to the general ledger without an approval step

38. A multi-account organization needs a shared platform service (an internal authorization API) reachable from workloads in 30 accounts, where every caller must present SigV4-signed requests authorized by IAM, and the platform team wants no VPC peering or Transit Gateway routes for this traffic. Which solution should be used?
    A. Share a VPC Lattice service network with AWS RAM, associate the consumer VPCs, and attach an IAM auth policy to the service
    B. Put the API behind an internet-facing ALB with a WAF
    C. Peer all 30 VPCs to the platform VPC
    D. Run a copy of the API in every account

39. The platform team must prove to auditors every quarter that the Region-failover runbook works, within the RTO, without disrupting production. Which combination is MOST appropriate? (Select TWO)
    A. Run an AWS FIS experiment that simulates loss of cross-Region connectivity in a pre-production copy of the stack, with stop conditions
    B. Execute the failover with Route 53 ARC routing controls in a game-day and measure the time to recovery, tracked in Resilience Hub
    C. Delete the primary Region's resources during business hours
    D. Rely on the DR plan document without exercising it
    E. Disable health checks so that failover cannot happen accidentally

40. A company's cost report shows Bedrock as the fastest-growing line item. Analysis shows most requests repeat the same 6,000-token system prompt and that simple questions are sent to the largest model. Which combination reduces cost the MOST with the least application change? (Select TWO)
    A. Enable prompt caching so the repeated system prompt is cached across invocations
    B. Move all inference to on-premises GPUs
    C. Use Bedrock intelligent prompt routing (or application logic) to route simple requests to a smaller model
    D. Increase the model's maximum output tokens
    E. Turn off guardrails to save invocation time

## Answers

| # | Answer | Why |
| --- | --- | --- |
| 1 | B | A Bedrock knowledge base does the RAG plumbing (chunking, embeddings, vector store, sync). Weekly fine-tuning is costly and does not give citations; stuffing 40,000 manuals into the context is impossible; a self-hosted vector DB is undifferentiated work |
| 2 | B | Guardrails are enforced outside the prompt and apply to every invocation and agent: denied topics plus sensitive-information filters (mask or block PII). Prompt instructions and regexes vary per team and can be bypassed |
| 3 | A | The contextual grounding check scores whether the response is grounded in the retrieved source and blocks ungrounded answers; temperature, Comprehend and throughput do not address hallucination |
| 4 | A,B | AgentCore Runtime is the managed, session-isolated agent host; AgentCore Gateway turns existing APIs and Lambda functions into MCP tools. EC2 fleets, WebSocket APIs and Batch are not agent-hosting primitives |
| 5 | B | AgentCore Identity handles inbound and outbound auth with OAuth and a secure token vault, so the agent acts with the user's delegated consent. A shared key, access keys or unauthenticated Cognito access break least privilege |
| 6 | B | waitForTaskToken pauses the workflow for up to a year until the approver's system returns the token; the money-moving Lambda runs only after that. Direct writes, sleeping Lambdas and "trusting the prompt" do not enforce the control |
| 7 | A | AgentCore Memory separates short-term (session) and long-term (cross-session) memory. Prompt stuffing, a cache TTL and fine-tuning do not give durable per-user memory |
| 8 | A,C | PrivateLink keeps Bedrock traffic on the AWS network with an endpoint policy; an SCP is the organization-wide ceiling on which models and Regions can be invoked. NAT, open security groups and Macie do not meet either requirement |
| 9 | A,C | Application inference profiles carry cost-allocation tags per unit; cross-Region inference profiles spread on-demand traffic over Regions. There are no Bedrock Reserved Instances and CloudTrail is not a billing source |
| 10 | B | Metadata filtering at Retrieve time is the designed way to scope results per tenant in a shared knowledge base. One knowledge base per tenant duplicates infrastructure; prompt instructions are not a security boundary; per-tenant KMS keys do not stop retrieval |
| 11 | A | AgentCore Observability emits OpenTelemetry traces and metrics to CloudWatch, and Bedrock publishes invocation and guardrail metrics that alarms can watch. Writing prompts to S3, Config rules and flow logs do not give traces or intervention rates |
| 12 | B | Resilience Hub compares the application against a resiliency policy (RTO/RPO) and produces a score with recommendations. Trusted Advisor, the WA Tool and DevOps Guru do not assess RTO/RPO per component |
| 13 | B | FIS runs controlled chaos experiments with scenario templates, and a CloudWatch alarm as a stop condition halts the experiment automatically. Manual termination has no automatic stop; load tests and permanent AZ removal are different things |
| 14 | A | ARC zonal shift moves traffic away from an impaired AZ in minutes for ALB/NLB (and EKS/EC2 ASG); zonal autoshift lets AWS do it when it detects impairment. Instance size, per-instance records and longer TTLs make the gray failure worse |
| 15 | A | ARC routing controls run on a five-Region cluster with its own data plane so failover does not depend on the failing Region, and readiness checks continuously verify the standby. A Lambda in the primary Region fails with it; CloudFront origin failover and manual DNS edits do not meet the requirements |
| 16 | A | Alarm to EventBridge to a Systems Manager Automation runbook gives an auditable, hands-off remediation that can call ModifyVolume and Run Command. Cron with sudo, bastions and instance replacement either need logins or lose data |
| 17 | B | EventBridge plus Step Functions gives event-driven, serverless orchestration with built-in Retry and Catch and a DLQ for failed inputs. Polling, nightly batch and a 24/7 consumer either miss the 15-minute target or run servers |
| 18 | A | Standard workflows run up to a year with exactly-once step semantics, built-in Retry with backoff and callback tasks. Express workflows are limited to 5 minutes and at-least-once; queue chains and MQ lack durable state and retries |
| 19 | B | VPC Lattice is the cross-account, cross-compute application network with IAM auth policies and no sidecars. App Mesh is a sidecar mesh in maintenance; full-mesh peering does not scale; public ALBs with API keys are not IAM authorization |
| 20 | A | Service Connect gives ECS-native discovery, retries and traffic telemetry with an AWS-managed proxy. App Mesh requires operating Envoy; CLBs and static IPs are not discovery |
| 21 | A,C | Enhanced scanning via Inspector rescans continuously and the pipeline gate blocks critical images; Signer plus an admission controller ensures only pipeline-built images run. Laptop scans, root containers and mutable tags weaken security |
| 22 | A | ABAC with session tags and dynamodb:LeadingKeys lets one role and one function serve all tenants while IAM enforces row isolation. Per-tenant tables and functions do not scale; application filters are not IAM enforcement; a shared admin role has no isolation |
| 23 | A | Kinesis plus Managed Flink gives sub-second stream processing; Firehose delivers the same stream to S3 in Iceberg for batch. RDS polling, FIFO with one consumer and daily Glue jobs cannot meet 2 seconds |
| 24 | A | Inspector's CI/CD integration scans SBOMs and images inside the build, can fail the stage on severity, and reports to Security Hub. Manual reviews, GuardDuty runtime and Macie are not build-time vulnerability gates |
| 25 | B | A tooling account with cross-account deployment roles (CDK Pipelines, StackSets service-managed permissions) is the reference pattern; the management account stays out of workload deployment. Admin in the management account, stored keys and root credentials violate least privilege |
| 26 | A,C | Container Insights with enhanced observability gives per-container and control-plane metrics; Managed Prometheus and Grafana are the open-standard managed stack. Cron kubectl, flow logs and Config do not provide container metrics |
| 27 | A,B | Bedrock publishes latency and token metrics to CloudWatch for alarms and budgets; SageMaker Model Monitor detects data-quality drift against a baseline. Reachability Analyzer, Trusted Advisor and Inspector are unrelated |
| 28 | A | RUM measures real browser sessions by page and geography; Synthetics canaries exercise the flow on a schedule and alarm even with no traffic. Weekly log review, a bigger ALB and a home-page health check miss both needs |
| 29 | A | Application Signals auto-instruments services and tracks SLOs with burn-rate alarms. Hand-written metrics, S3 logs and Trusted Advisor do not provide SLO tracking |
| 30 | A | Iceberg on S3 in the Glue catalog gives ACID, schema evolution and time travel across Athena, EMR and Redshift; Lake Formation adds column-level and LF-tag permissions. CSV, nightly Redshift copies and EBS Hadoop lack these |
| 31 | B | Lake Formation cross-account grants (via RAM) share tables and columns in place; consumers create resource links. Replication, public buckets and emailed CSVs copy data and lose governance |
| 32 | A | Clean Rooms runs joint queries under analysis rules so neither party sees the other's raw rows; differential privacy adds further protection. Shared buckets, replicas and DataSync all expose raw data |
| 33 | A | Firehose can write directly into Iceberg tables, so one pipeline serves both near-real-time and historical queries. DynamoDB exports, split pipelines and RDS do not meet the single-table requirement |
| 34 | A | ML-DSA is the NIST post-quantum signature standard that KMS offers as a key spec for sign and verify. RSA and ECDSA are vulnerable to Shor's algorithm; SSE-S3 is encryption, not signing |
| 35 | A | Hybrid post-quantum TLS combines classical key exchange with ML-KEM so recorded sessions cannot be decrypted later; AWS supports it on KMS, ACM and Secrets Manager endpoints via supporting SDKs. Timeouts, plaintext and key rotation do not protect the recorded TLS session |
| 36 | A | ML-KEM (FIPS 203) is the key-encapsulation mechanism; ML-DSA (FIPS 204) is the digital-signature algorithm. Neither replaces AES for data at rest |
| 37 | A,C | Scoped knowledge base, a guardrail (denied topic plus PII masking) and a Step Functions approval before the money-moving tool, with log data-protection so account numbers never land in logs. A shared admin user, public prompts and unapproved ledger writes fail the requirements |
| 38 | A | A RAM-shared VPC Lattice service network with an IAM auth policy gives cross-account, SigV4-authorized access without peering or TGW routes. Public ALBs, full-mesh peering and per-account copies do not meet the requirements |
| 39 | A,B | FIS proves the behaviour safely in pre-production with stop conditions; a game-day using ARC routing controls measures real recovery time, which Resilience Hub can track. Deleting production, an unexercised document and disabled health checks are not evidence |
| 40 | A,C | Prompt caching removes the cost of the repeated system prompt; routing simple requests to a smaller model cuts per-token cost. On-premises GPUs are a large change; more output tokens and removing guardrails raise cost or risk |
