import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
 
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
        
prompt = """Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking,
then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.
The question is: what is the ideal weather condition in australia?"""
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
)
print(response.choices[0].message.content)


Output:
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
