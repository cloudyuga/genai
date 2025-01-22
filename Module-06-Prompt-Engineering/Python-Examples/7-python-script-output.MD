## 1. Output of Zero-shot prompt:
python .\zero-shot-prompt.py
Beneath the sky where seagulls roam,  
The ocean sings its ancient tome.
Its waves, like whispers, brush the shore,
A lullaby that calls for more.

The sun dips low, a fiery hue,


## 2. Output of few-shot learning prompt:
python .\few-shot-learning-prompt.py
"I love programming." -> "J'adore la programmation."


## 3. Output of contextual prompt:
python .\contextual-prompt.py       
Enter the context (provide detailed background information): The time from Britain's first inhabitation until the Last Glacial Maximum is known as the Old Stone Age, or Palaeolithic era. Archaeological evidence indicates that what was to become England was colonised by humans long before the rest of the British Isles because of its more hospitable climate between and during the various glacial periods of the distant past. This earliest evidence, from Happisburgh in Norfolk, includes the oldest hominid artefacts found in Britain, and points to dates of more than 800,000 RCYBP.[1] These earliest inhabitants were hunter-gatherers. Low sea-levels meant that Britain was attached to the continent for much of this earliest period of history, and varying temperatures over tens of thousands of years meant that it was not always inhabited.
Enter the question (what do you want to know?): what is old stone age?

Response:
The Old Stone Age, or Palaeolithic era, is the earliest period of human history characterized by the use of stone tools. It spans from the first appearance of hominins over 2 million years ago until approximately 10,000 years ago, leading up to the end of the Last Glacial Maximum. During this time, humans were primarily hunter-gatherers, relying on foraging and hunting for survival. In Britain, archaeological evidence suggests that this period began with the inhabitation of the region over 800,000 years ago, facilitated by varying and more hospitable climatic conditions during glacial and interglacial periods.


## 4. Output of prompt with constraints:
python .\prompt-with-constraints.py
Climate change refers to long-term alterations in temperature, precipitation, and other atmospheric conditions, primarily attributed to human activities such as fossil fuel combustion and deforestation. It poses significant environmental challenges, including increased frequency of extreme weather events, rising sea levels, and biodiversity loss, necessitating urgent global cooperation to mitigate its effects.


## 5. Output of COT
python .\chain-of-thought.py
To determine how many apples Tom has after the transactions described, we can break it down step by step:

1. **Initial Number of Apples**: Tom starts with 12 apples.

   \[
   \text{Apples with Tom} = 12
   \]

2. **Giving Apples to Jerry**: Tom gives 4 apples to Jerry. To find out how many apples Tom has after this, we subtract the 4 apples he gave away from his initial amount.

   \[
   12 - 4 = 8
   \]

   Now, Tom has 8 apples left. 

3. **Buying More Apples**: Next, Tom buys 7 more apples. To find Tom's new total after buying these apples, we add the 7 apples to the 8 apples he had after giving some to Jerry.

   \[
   8 + 7 = 15
   \]

   Now, Tom has 15 apples.

4. **Giving Apples to Sally**: Finally, Tom gives 5 apples to Sally. We need to subtract these 5 apples from the 15 apples he currently has.

   \[
   15 - 5 = 10
   \]

After all the transactions, Tom has 10 apples left.

So, the final answer is:

\[
\text{Tom has } 10 \text{ apples now.}
\]


## 6. Output of tree of thoughts:
python .\tree-of-thoughts.py
### Expert 1: Climatologist

**Step 1:** Assess the general climate zones in Australia, which range from tropical in the north to temperate in the south. Acknowledge that the ideal weather condition may vary based on these different regions.

### Expert 2: Agricultural Scientist

**Step 1:** Consider the ideal weather conditions for agriculture, which would include ample sunlight, moderate temperatures, and adequate rainfall to ensure healthy crop growth while avoiding extremes of heat and drought.

### Expert 3: Meteorologist

**Step 1:** Evaluate the importance of stability in weather conditions. Ideal weather would likely involve consistent temperatures and limited variation in rainfall, aiming for low humidity and gentle winds to ensure comfort and safety.

---

### Expert 1: Climatologist

**Step 2:** Identify the specific regions in Australia that are best suited for these ideal conditions. For example, areas like the southern part of Australia might have milder and more consistent temperatures that would be desirable for many activities.

### Expert 2: Agricultural Scientist

**Step 2:** Highlight that the timing of seasonal weather is critical for agriculture. Ideal conditions would also mean having predictable seasons with sufficient rain during the growing season and drier, warmer conditions during harvest time.

### Expert 3: Meteorologist

**Step 2:** Determine that there would be a temperature range that is most comfortable for Australians, likely between 20-25 degrees Celsius, with minimal outliers to prevent extreme weather events such as heatwaves or flooding.

---

### Expert 1: Climatologist

**Step 3:** Discuss the effect of climate change on these ideal conditions. Consider that shifting weather patterns may mean that previously ideal conditions are becoming less frequent, which affects multiple regions across Australia.

### Expert 2: Agricultural Scientist

**Step 3:** Explore the necessity of resilience in weather patterns, emphasizing that while rainfall is important, drought resistance and the ability of crops to thrive under varying conditions must also be part of the ideal scenario.

### Expert 3: Meteorologist

**Step 3:** Acknowledge the need for ideal weather to not only maintain stability but also to prepare for extreme weather events. This would involve looking into historical weather trends to identify the fluctuations and understand how they impact the current ideal conditions.

---

### Expert 1: Climatologist

**Step 4:** Conclude that ideal weather conditions in Australia, while varied, may reside in temperate regions during spring and autumn, marked by moderate temperatures and reliable rainfall patterns.

### Expert 2: Agricultural Scientist

**Step 4:** Suggest that ideal crop yield weather conditions typically occur in the Mediterranean climate regions of Australia, particularly in the southwest where summers are dry and winters are rainy.

### Expert 3: Meteorologist

**Step 4:** Postulate that the criteria for ideal weather must include considerations of public safety, with a focus on ensuring sustainable weather patterns that can accommodate recreational and domestic activities throughout the year.

---

All experts have formulated comprehensive views, and upon reviewing each other's perspectives, they find consensus on the key attributes of ideal weather conditions, while also recognizing regional variations and challenges posed by climate change. None of the experts have identified a mistake in their reasoning, so all remain engaged in the discussion.

