# Model Selection: Exploring the AI Toolkit Model Catalog

In this section, you will explore the AI Toolkit Model Catalog to discover, filter, and compare models for your multimodal agent project. The Model Catalog provides access to models from various providers including GitHub, Microsoft Foundry, OpenAI, and others.

## Step 1: Apply Filters to Narrow Your Selection

1. Locate the **AI Toolkit** extension icon in the left sidebar
2. Click on the AI Toolkit icon to open the extension panel
3. Under **Developer Tools**, expand the **Discover** section and click on **Model Catalog** to open the catalog interface

![Model Catalog](../../img/model_catalog.png)

On the top of the page you'll find the most popular models; scroll down to see the full list of available models.

Since the list is quite consistent, you can use the filtering options to narrow down the selection based on your requirements.

![Filter Options](../../img/filter_options.png)

### Filter by Hosting Provider

1. Click on the **All Filters** filter dropdown to display the `Hosted by` list. You have several options, such as GitHub (providing free-to-use token-rate limited models), Microsoft Foundry, OpenAI, and you can even leverage models hosted on your local infrastructure, through Ollama or ONNX.

2. Select **Microsoft Foundry** to view models hosted in Microsoft Foundry, which provide enterprise-grade security and compliance features, ideal for enterprise applications.

### Filter by Publisher

1. Continue to scroll down the filter list until you reach the **Publisher** section and select **Meta** to view models from this leading provider.

### Filter by Model Feature

1. Continue to scroll down the filter list until you reach the **Feature** section to filter by model capabilities, such as image/audio or video processing, tool calling, etc.
2. Select **Image Attachment** to find multimodal models that support visual input processing and enables multimodal interactions combining text and images.

## Step 2: Deploy Models to Your Subscription

After applying filters, you'll see a refined list of models.
Locate **Llama-4-Maverick-17B-128E-Instruct-FP8** in the filtered results. It's a multimodal model with good reasoning capabilities.

2. Click **Deploy** on the model tile to open the deployment configuration window.  

![Add Model](../../img/add_model.png)

3. Drag the slider of the **Token Per Minute** rate to the right to increase it to 120K. Leave the other parameters as default and click on **Deploy to Microsoft Foundry** to provision an instance of the model to your subscription.

![Deployment Configuration](../../img/deployment_configuration.png)

## Step 3: Open the Playground for Testing

1. In the left sidebar, locate the **My Resources** section and expand the resources under your Microsoft Foundry project.
1. Under the **Models** section, you should see the model instance you just deployed. You should also see a pre-deployed instance of **gpt-5.3-chat** for comparison testing later on and an instance of **text-embedding-3-small** that we will use in the next section for vector search and retrieval augmented generation.
1. Right-click on the model instance you just deployed and then select **Open in Playground** from the dropdown menu to start testing the model in the Playground interface.
![Try in playground](../../img/try_in_playground.png)

2. In the **Model** field, you'll see the name of the model you just selected. 

![Model Playground](../../img/model_playground.png)

> [!WARNING]
> You might experience some delay in model loading, especially if it's your first time accessing the Playground. Please be patient while the model initializes.

3. Next, click the **Compare** button to enable side-by-side comparison
4. From the dropdown, select **gpt-5.3-chat** deployment that has been pre-deployed for this workshop in Microsoft Foundry
5. You now have two models ready for comparison testing

![Model Comparison](../../img/model_comparison.png)

## Step 4: Test Text Generation and Multimodal Capabilities

> [!TIP]
> The side-by-side comparison allows you to see exactly how different models handle the same input, making it easier to choose the best fit for your specific use case.

Let's start interacting with the models with a simple prompt:

1. Enter this prompt in the text field (where you see the placeholder "Type a prompt"):

```
I’m a store manager at a DIY retailer. What are the most important metrics to review in a weekly sales summary, and why?
```
2. Click the paper airplane icon to execute the prompt on both models simultaneously

![Test the model](../../img/test_the_model.png)

Now let's test their reasoning capabilities, with the following prompt:
```
We have 3 stores (A, B, C). We only have 40 circuit breakers total across all stores and replenishment arrives in 10 days.

Here’s a simple snapshot of sales trend and stock on hand:

| Store | Sales trend (WoW) | Avg weekly units sold | Current stock (units) |
|------:|-------------------:|----------------------:|----------------------:|
| A     | +30%              | 18                    | 8                     |
| B     | 0%                | 10                    | 22                    |
| C     | -15%              | 7                     | 10                    |

How should we allocate stock today to minimize stockouts and lost sales? Explain your reasoning step by step, and list the 3 most important additional data points you would ask for.
```

Next, test the models' image processing capabilities:

1. Enter this prompt in the text field:
```
In Japanese, describe what's in this image and what kind of electrical component it appears to be.
```

2. Click the image attachment icon to add a picture as input

![Image Attachment](../../img/image_attachment.png)

3. You'll be prompted with a browsing window to select the image file attachment to upload. Navigate to the following location:
```
C:\Users\LabUser\aitour26-WRK542-prototype-agents-with-the-ai-toolkit-and-model-context-protocol\src\instructions
```
Then select the file named **circuit_breaker.png** and click **Open**.
![Image File Path](../../img/image_file_path.png)

4. Send the multimodal prompt on both models simultaneously.

## Step 5: Analyze and Compare Results

Review the outputs from both models, using several factors to guide your evaluation:

- **Response Quality**: Compare the depth and accuracy of descriptions, as well as the coherence with the input prompt.
- **Detail Level**: Which model provides more comprehensive analysis?
- **Processing Time**: Note any differences in response speed.
- **Output Formatting**: Evaluate clarity and organization of responses, as well as verbosity. Note that the verbosity of the model influences token usage and cost.

### Leverage GitHub Copilot for Comparative Analysis

To assist with the comparative analysis, you can leverage GitHub Copilot to generate a comparison summary.

To access GitHub Copilot Chat, select the **Toggle Chat** icon at the top of the Visual Studio Code window.

![Toggle chat button.](../../img/toggle-chat.png)

Select `Auto` then select `Other models` - to pick *Claude Opus 4.5*.

> [!TIP]
> Expand the 'Other models' section in the dropdown to find the Claude Opus 4.5 model, if you cannot see it in the main list of models.

![Select claude Opus 4.5](../../img/select_claude_opus.png)

> [!WARNING]
> If you are not logged in, you won't be able to select the model. Ensure you have completed the GitHub Copilot sign-in process as per previous lab section or send a prompt to trigger the sign-in flow.

Try the following prompt in the Copilot chat window:

```
#mcp_azure_mcp_foundry I am exploring models for an AI agent that should support Zava - a DIY retailer with 20 stores across the United States and an online channel - on store operations and head office sales analysis. I am evaluating Llama-4-Maverick-17B-128E-Instruct-FP8 and OpenAI GPT-5.3-chat. Which one would you recommend for this scenario, and why? Explain the trade-offs between models (e.g., reasoning ability, cost, latency, context length) so that I can make an informed choice.
```

To answer this, Copilot leverages the *Foundry MCP server* tools, which provide model recommendations based on your use case. If asked for approval to allow Copilot to access the Foundry MCP server tools - click **Allow in this session** to proceed. This might happen multiple times, as Copilot may need to access several tools to gather the necessary information for the analysis.

![Get AI model guidance](../../img/get_ai_model_guidance.png)

In the final response, you should see a detailed comparison between the two models, along with a recommendation on which one to select for your AI agent project.

## Step 6: Import selected model from Microsoft Foundry

Once we are done with the comparison, we are going to select one of the two models for further prototyping in the next lab sections. For the sake of this exercise, let's go with **GPT-5.3-chat**.

> [!TIP]
> To come back to the standard Playground (with a single pane and a single model),you can click on **Select this model** on the right side of the model name.
>
> ![Select this model](../../img/select_this_model.png)

## Key Takeaways

- The Model Catalog provides a comprehensive view of available AI models from multiple providers
- Filtering capabilities help you quickly identify models that match your specific requirements
- Model comparison in the Playground enables data-driven decision making
- Different hosting options offer varying benefits for different stages of development
- Multimodal capabilities can be tested effectively using the built-in comparison tools

This exploration process ensures you select the most appropriate model for your specific use case, balancing factors like performance, cost, features, and deployment requirements.
Click **Next** to proceed to the following section of the lab.
