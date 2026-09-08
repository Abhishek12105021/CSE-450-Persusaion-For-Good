# Manual re-check: the 81 dialogues that flipped yes -> no

This report covers every dialogue where the old scheme's `binary_label` was `yes` but carried a `conditional` or `deferred` modifier, and which therefore became `no` under the new single-field strict rule (`Dataset_updated/annotation_guidelines.md`). Each of the 81 was **read in full**, by hand, directly from `dialogue_text` in `Manual_Label.csv` - no keyword or regex matching was used to produce these verdicts.

**Question asked per dialogue:** does the Persuadee's *final, resolved* position read as a fully clear, unconditional commitment (no "if/maybe/might/probably/would consider/I'll think about it" attached to it), even though the old annotator tagged it `conditional`/`deferred`?

## Outcome — action taken

Following manual review, **37 of the 81 dialogues were reverted back to `yes`** in both `Dataset_updated/Manual_Label.csv` and `Dataset_updated/donation_intetion_manual_label_dataset.csv`. The remaining **44 stay `no`**, confirming the original flip.

| | Count |
|---|---|
| Flipped yes -> no under the new rule, then reviewed | 81 |
| **Confirmed correct — left as `no`** | 44 |
| **Reverted back to `yes`** | 37 |

Dataset-wide effect: the strict-rule relabel had produced 657 `yes` / 360 `no`. After this correction pass, the dataset now stands at **694 `yes` / 323 `no`** across the 1,017 dialogues. Both dataset files were verified to agree with each other on every dialogue after the change, and no other column (`text`, `context`, `dialogue_text`, row order) was touched.

**Why so many reverted.** Reading through all 81 in full, a recurring pattern emerged: the original annotator tagged a dialogue `deferred` (or `conditional`) based on something said *earlier* in the conversation, but the Persuadee's dialogue often continued and resolved into a clean, unhedged commitment before the end - and the modifier tag was never revisited. Under the guideline's own rule of thumb #2 ("use the Persuadee's last clear position"), these read as legitimate `yes` cases once the ending is taken as authoritative rather than the earlier hedge.

A smaller sub-pattern among the reverted cases (flagged individually below) involves dialogues that never explicitly say the pledged amount comes out of *this task's* payment - the commitment itself is clean, but whether it is an in-task commitment at all is a separate question worth a second look independently of this pass.

---

## Part A — Confirmed correct, left as `no` (44)

### 1. `20180723-080248_452_live`  —  old modifier: `conditional`

**Why:** Never resolves into a commitment at all. Final line: "hmmm, let me think about it." No amount, no yes.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello! Ho are you doing today?
[Persuadee] doing fine, what about you
[Persuader] I'm doing great but i would feel so much better if you let me tell you about one amazing charity
[Persuadee] go ahead :) i'm listening
[Persuader] I'm working for Save the Children charity! Have you heard about it?
[Persuadee] I don't think so. 
[Persuader] It's a great charity that helps children i developing countries and they are also currently helping at the US Mexican border to reunite children with their families
[Persuadee] such an important job! Tell me more
[Persuader] Sure! There was this little boy in Africa, he was only 1 year old and he died of hunger. It breaks my heart
[Persuadee] so sad. How can i help?
[Persuader] i'm glad you asked! you can help save children like that boy by donating to Save the Children
[Persuadee] how do i know money will go to children and it's not a scam?
[Persuader] This charity is one of the most top rated in the world. You can also check out their website to see for yourself  URL 
[Persuadee] great, let me check it out
[Persuader] sure! Take your time. I'm here whenever you are ready
[Persuadee] so i like that 86% is going to the cause. 
[Persuader] yes! You see? This charity is credible and people who work for it are professionals and have big hearts. would you like to donate and save the children?
[Persuadee] I probably will. Is there a minimum i can donate?
[Persuader] you can donate as much as 2$ or as little as couple of cents. I encourage you to donate as much as you can
[Persuadee] hmmm, let me think about it
```
</details>

### 2. `20180723-120746_371_live`  —  old modifier: `conditional`

**Why:** Negotiates a $30 one-time PayPal donation but never finalizes it; ends on "I do have a few questions first" -> "that sounds great." No confirmed act of donating.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello would you please donate to help save the children?
[Persuadee] What children organization?
[Persuader] This organization is called Save the Children and your donation can help ensure children't rights to health, education, and safety.
[Persuadee] How long has this charity been around?
[Persuader] We have been around for a long time and have worked hard to ensure that as much of your money as possible goes towards helping the children. The children need your help to ensure that they have a fighting chance at their future. You can help care for them medically and ensure they have the education needed to succeed in life.
[Persuadee] The organization sounds like a good one. What is a typical donation?
[Persuader] Through child sponsorship, you can change a child's life, as well as your own _ all for about $1 a day. This is the most popular donation. We also have where you can set up a monthly donation or make a one time donation.
[Persuadee] I think I would be interested in the child sponsorship.
[Persuader] That sounds amazing! You will help make a child's dreams come true! Would you like to set up a one time donation for $30 or would you prefer to do it monthly? We can accept all major credit cards and Paypal for your convenience. Which would you prefer?
[Persuadee] A one time donation would be best.
[Persuader] We appreciate your help in Saving the Children! How would you like to make payment for this donation? We can accept all major credit cards and Paypal for your convenience.
[Persuadee] Paypal is usually my choice.
[Persuader] It is a great choice. All I need is your Paypal email and I will submit a request for the donation so that all you have to do is accept it. Does that sound ok to you?
[Persuadee] I do have a few questions first.
[Persuader] Yes, what questions do you have?
[Persuadee] Where is the charity based out of?
[Persuader] Our headquarters is based out of Fairfield, CT and we service children all over the world.
[Persuadee] Okay, where are the major areas you serve?
[Persuader] We have several programs throughout the US to help children here. We also over several outreach programs in countries around the world. Where we serve depends on where the needs are greatest and/or if there are any emergency situations.
[Persuadee] that sounds great.
```
</details>

### 3. `20180826-020520_686_live`  —  old modifier: `conditional`

**Why:** "yes i sure will do donate. after i die i will donate my all.." - the only "yes" is about donating after death, not within this task. Earlier: "maybe i will do."

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello! What if i told you that you have the opportunity of a lifetime to make a change in the world? Would you take it?
[Persuadee] i will like to know about the opportunity first 
[Persuader] Well, the opportunity would be able to help fight world hunger by donating to Save the Children. Would you do it now?
[Persuadee] powerful people cause war and war cause hunger, and we average people sit on our chair try to donate some money to the poor 
[Persuader] It benefits every where not just war torn countries
[Persuadee] i get that. 
[Persuader] The best part is knowing that you can help make a change in a person's life who is currently unable to financially
[Persuadee] yeah i know how donation works. I have 300000 immigrants in my country. we helping a person to better their life this is what we humans do 
[Persuader] Actually, it is a lot more than that because the "true" Americans are the Native Indians. Everyone else came from Europe or Africa
[Persuadee] where do you came from?
[Persuader] So in hindsight we are all immigrants who need a little charity from time to time.
[Persuadee] charity is a bad for that. 
[Persuader] Have you ever made a donation that you have been proud to be a part of?
[Persuadee] yeah i did. but it never reached to the people i heard so far
[Persuader] Well, if you make a donation to Save the Children i can gaurantee that you will know where it goes. Would you donate then?
[Persuadee] maybe i will do
[Persuader] That's great to hear. What amount were you thinking of donating? It can be as much as you want.
[Persuadee] have you ever done any donation to this charity?
[Persuader] I sure have, that is why i can cofidently say that now only will your money be going where you want it to but it will be put to good use when it gets there.
[Persuadee] yes i sure will do donate. after i die i will donate my all..
[Persuader] How much would you like to donate today?
```
</details>

### 4. `20180826-072151_442_live`  —  old modifier: `conditional`

**Why:** Final line is explicitly conditional and never independently confirmed: "i can donate 5 if you truly are donating 5."

<details><summary>Full dialogue text</summary>

```
[Persuader] Are you aware of Save the children Organization?
[Persuadee] yes i know that is a good charity foundation, they help the children.
[Persuader] I saw a children die once
[Persuadee] what? what happened? 
[Persuader] He was hungry with no food.I was serving in Afghanistan 
[Persuadee] you were in military? why did not you help him?
[Persuader] Yes.I tried to give him my food but it was too late
[Persuadee] he was in the end i think, this is the kind of things i have about our civilization , many dnt have to eat and many waste their food, its not right
[Persuader] Exactly.More than thousands children have died of hunger in Syria this year.We must do something about it
[Persuadee] for sure we must do something, but many people are blind, they see just the green of the money, they dont interact with people to see whats their problems are, i really want to help go in africa or some place but i dont know how i can go with a organization.
[Persuader] Donate to Save the Children.They are a blessing to humanity
[Persuadee] this i can do, but i was thinking about actual helping.
[Persuader] Thats actual help.They really make a difference.I see it with my own eyes
[Persuadee] yeah i know that they are helping Hawaii now , with the hurricane coming soon.
[Persuader] Yes they are.How much money do you spend on candies?
[Persuadee] 5$ maybe, plus minus, why?
[Persuader] Because you can use some of that money to donate to Save and Children?
[Persuadee] of course i would donate, how much are you willing to donate?
[Persuader] I willing to donate 5.And You?
[Persuadee] i can donate 5 if you truly are donating 5. im happy to help
```
</details>

### 5. `20180826-184708_183_live`  —  old modifier: `conditional`

**Why:** Ends on suspicion of the Persuader's tactics: "Why the aggressive tone of me 'donating or not'?" No commitment ever made.

<details><summary>Full dialogue text</summary>

```
[Persuader] hello?
[Persuadee] Hello there!
[Persuader] Would you like to donate to Save the Children?
[Persuadee] Yes, what would this charity be doing to save the children?
[Persuader] Save the Children is and how their donation is essential to help ensuring children's rights to health, education, safety, etc. 
[Persuadee] What have they done in the past? 
[Persuader] Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries.
[Persuadee] What countries have they been able to help? 
[Persuader]  Millions of Syrian children have grown up facing the daily threat of violence. In the first two months of 2018 alone, 1,000 children were reportedly killed or injured in intensifying violence.
[Persuadee] I am aware of the violence in Syria but what has "Save the Children" done to aid in health, education and safety?
[Persuader] Small donations will indeed help a lot of children and their families. How much would you like to donate?
[Persuadee] Before I can donate I will need to know how this organization has help. 
[Persuader] Be specific in what your asking?
[Persuadee] How has "Save the Children" helped to aid in health, education and safety of the Syrian children?
[Persuader] Save the children send over rights to health, education, and safety with the funds that you donate to developing countries Syria was an example of countries we aid with the donation. Would you like to donate?
[Persuadee] Send over rights? I do not understand. I also agreed to donate but before that I need more information, why do you keep asking me to donate? 
[Persuader] Because you keep asking the same question for someone that conversing about donating to a charity. Its almost like you want to see paper work proof, I told you where your donation goes either you want to donate or not?
[Persuadee] Exactly, in today\'s world one must be weary of scammers. Those who are really trying to do "good" for others will be more than happy to show proof of where donations are going or at least letting one know how those donations will be put to use. Telling me where it goes really does nothing for me. 
[Persuader]  URL go check it out.
[Persuadee] Why the aggressive tone of me "donating or not"?
```
</details>

### 6. `20180826-192022_0_live`  —  old modifier: `conditional`

**Why:** Ends with the Persuader asking for an amount and no reply given. Last Persuadee lines are only appreciation for information, no commitment.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello, may I ask how interested are you in children and their quality of life right now
[Persuadee] I am very interested! I think it is important to support children from all walks of life.
[Persuader] Have you ever thought about donating to an organization that helps children in need?
[Persuadee] I absolutely have, most recently to support children who were separated from their parents entering the country.
[Persuader] That is great to hear, but sadly there is not much that that organization can do, as a lot of children in poor countries don't even get the chance to live past the 15 years of age
[Persuadee] Is there a particular organization or charity you are thinking of?
[Persuader] Yes, it is called Save The Children, it is an organization dedicated to ensure safety, education, health and other basic needs for kids in poor countries
[Persuadee] That sounds very interesting. What sorts of things do they do to ensure those things? And what countries do they provide support in?
[Persuader] They mostly help kids in the African continent, but also in Asian countries like Nepal and Butan, where there is simply no way for kids to access education unless their parents are rich. They work hand in hand with the red cross and UNICEF to bring help to those in need, often aiding personally with their voluntaries besides cooperating with the money
[Persuadee] Wow that is amazing! How long has this organization been volunteering?
[Persuader] They are about to celebrate their 10th anniversary next year
[Persuadee] That sounds like they have a pretty strong foundation. I like that they provide educational support for the children. 
[Persuader] I like that too, perhaps you would be interested in donating something to them?
[Persuadee] I might be interested. What ways can I donate?
[Persuader] You can visit their site to do so, or visit one of their physical locations if they are nearby
[Persuadee] Do you know where they have offices?
[Persuader] They have offices in most cities of USA and Canada, if you are not near, you can always visit their website
[Persuadee] I will definitely have to check their website out. Do you know if they support children in the US who do not have access to education or other basic necessities?
[Persuader] They do most probably, they care for al children in need equally
[Persuadee] That is wonderful, thank you for all the information.
[Persuader] So, how much would you like to donate to this organization?
```
</details>

### 7. `20180831-175925_143_live`  —  old modifier: `conditional`

**Why:** Ends still skeptical: "how do i know that?" No commitment is ever made before the dialogue ends.

<details><summary>Full dialogue text</summary>

```
[Persuader] hi how are you?
 [Persuadee] good how are you?
 [Persuader] fine today...do you have children?
 [Persuadee] no i do not
 [Persuader] Do you like children?
 [Persuadee] yes of course
 [Persuader] Do you want to help children?
 [Persuadee] yes how would i do that?
 [Persuader] Do you want to help poor children without food?
 [Persuadee] yes i would 
 [Persuader] Do you want to help children without resources get an education?
 [Persuadee] yes i woulf
 [Persuader] How much in dollars would help a child in a poor country with basic needs?
 [Persuadee] what charity am i donating to?
 [Persuader] have you heard of save the children?
 [Persuadee] no i havent
 [Persuader] Are you worried about donating to charities
 [Persuadee] yes because i dont know where my money will be going
 [Persuader] right, save the children is legitimate for sure, can you donate one dollar a day to help a needy child?
 [Persuadee] how do i know that?
 [Persuader] check out save the children on the web , you will find it easy..thanks for the help!
```
</details>

### 8. `20180831-182245_152_live`  —  old modifier: `conditional`

**Why:** Firm, resolved $1.50 now ("I'll give $1.50 to Save the Children"), but the Persuadee's actual last statement adds a separate hedge about the future: "I will do some research on Save the Children and consider supporting them." Matches the guideline's own worked example (firm-now + vague-more-later = no).

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello! How are you?
 [Persuadee] Hello, fine, thanks! My name is Billy. How are you today?
 [Persuader] I am Elvir! Im doing great today, thanks for asking! Do you know about any NPOs? (Non-profit)
 [Persuadee] Nice to meet you, Elvir. I am familiar with NPOs 0 i even volunteer for one. How about you?
 [Persuader] I am a frequent donator to NPOs. What is the NPO that you volunteer for?
 [Persuadee] That is nice to hear. From time to time I volunteer for a tiny NPO school that teaches economics and social science to adults. 
 [Persuader] Oh nice! Is it local in your area?
 [Persuadee] Yes, although there are several similar schools around the US and across the world. What type of organizations do you support, Elvir?
 [Persuader] I support NPOs that engage in promoting childrens rights, providing relief and helping support children in developing countries. One NPO mainly being Save the Children.
 [Persuadee] That is wonderful. I am slightly familiar with Save the Children. Do you think that they are effective?
 [Persuader] They are very effective at their mission, making an international impact with professional and cautious use of the donation they receive. They are one of few NPO's who actually use their funds for their purpose.
 [Persuadee] Yes, mis-use and waste is a huge problem in with NPOs. For this reason I like and support Smile Train - they repair cleft lips using local resources. 
 [Persuader] Thats awesome! The amazing thing about the Save the Children mission is that 77 cents only can host a child in need for shelter for one day!
 [Persuadee] That is very cheap. Good nutrition, medical care, and a clean and safe environment are vital for all, especially children. 
 [Persuader] You will be recieving $2 for the survey completion, would you like to donate any of your compensation to Save The Children organization? It will go a long way for the children!
 [Persuadee] Yes, I would like to help out. There are many more needy than me. I'll give $1.50 to Save the Children. 
 [Persuader] Awesome! Thank you so much for your donation! At the end of the survey it will give you an option to donate that amount. This was a good talk!
 [Persuadee] Yes, I learned from you. I will do some research on Save the Children and consider supporting them. 
 [Persuader] Yes please do! I am a frequent donator of Save the Children! It was my pleasure, have a good day!
 [Persuadee] You too, Elvir. Have a great weekend and thanks again for the information on Save the Children.
```
</details>

### 9. `20180831-205301_781_live`  —  old modifier: `conditional`

**Why:** The Persuadee never personally commits to any amount. The only "I'm going to donate" statement in the whole dialogue belongs to the Persuader, not the Persuadee.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello. How are you? 
 [Persuadee] I'm doing well. It's getting late, it's been a long week. How are you?
 [Persuader] I'm doing good. I understand about the long week. Thank goodness it's the weekend. 
 [Persuadee] That's right! I'm actually up and at it bright and early to take a road trip for a family member's birthday tomorrow... joy. What do you have planned for the weekend?
 [Persuader] We're planning to hit the beach, but it's a shame that there are so many kids in poverty who won't be able to enjoy the beach or birthday parties. Don't you agree?
 [Persuadee] That really is a shame. I was fortunate enough to grow up 10 minutes from a beach regardless of my financial situation, but so many kids have no means to even take public transportation to a beach if they wanted to. Very unfortunate. I always hope those kinds are able to make a better situation of their lives as they get older to make up those experiences.
 [Persuader] I agree. We live near the beach right now too, and it's great. My kids are so fortunate to be living a life so far removed from war zones like kids in Syria. And, to have their basic needs met to be able to enjoy their childhood. Have you heard of Save the Children?
 [Persuadee] I'm sure I have, but could you give me a refresher?
 [Persuader] It's an awesome nonprofit that helps fight for children's rights all over the world. URL has a lot more information. 
 [Persuadee] I'll have to dig further into it. Do you know anything about who runs it? My biggest concerns with organizations like that is there isn't a ton of transparency as to where donation funds actually go.
 [Persuader] Oh, I totally understand. I feel like most of those organizations take the money and run. Save the Children actually has 86% of the money that is donated directly helping the children. It's listed on Forbes list of top 50 charities. 
 [Persuadee] Wow, that's great. I consider Forbes pretty trustworthy. I appreciate you getting that info for me. I'll have to dig further into their mission statements and activities. Some of that stuff can get so political!
 [Persuader] They also have their annual financial report actually listed on their website which I think is pretty impressive for a charity organization. Would you consider donating part of your pay for this task to Save the Children?
 [Persuadee] I would, but I think I'd have to review all of their documentation first and then possibly even donate on my own time! That's not to say I'm uninterested, I just like to trust and verify.
 [Persuader] I understand. It's important to do research before giving money to organizations. This one just seems like they're doing a lot of great work helping children in the U.S. and abroad. And, it would be so easy to have your payment taken directly from your task payment.
 [Persuadee] 100% agreed. I'll have to dig into their information and make a decision. Have you donated to them before or do you plan to?
 [Persuader] I haven't in the past, but after reading more about them I definitely plan to. Their credentials are outstanding. And, I like that so much of their proceeds actually go to help. I've seen some awful numbers from organizations like Goodwill who claim to be helping but all of their money actually goes to their CEO's.
 [Persuadee] You think Goodwill is bad, look at some of the reports on Susan G Komen--BREAST CANCER of all things. What starts with a good intention doesn't always end up that way. Does Save The Children specifically aim to help Syrian chidren?
 [Persuader] Oh, really? I haven't heard about Susan G Komen being so bad, I will have to look into that. I did a race of theirs about 10 years ago. 
 [Persuadee] I can\'t speak for 10 years ago, but I know recently they were found out to have so much of their money going to "marketing" that a massive portion of their proceeds never even made it to research. That\'s off the top of my head, but it\'s rough. I\'ve done a Donna race before, though.
 [Persuader] That's awful. That's why I'm pleasantly surprised to see that Save the Children has such a high percentage of donations being used. And, no. They don't only help in Syria. They support kids all over the world by helping them get healthcare, education, making sure their safe, etc. I'm going to donate part of my proceeds. I think you should too!
```
</details>

### 10. `20180831-211130_630_live`  —  old modifier: `conditional`

**Why:** Final line is an explicit deferral outside the task: "I just prefer to give on my own time." Also declines the in-task donation mechanism outright.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi How are you?
 [Persuadee] Hello, I am great, how are you?
 [Persuader] I'm great as well! Have you by chance ever heard of an organization called Save the Children?
 [Persuadee] Yes I have heard of them.
 [Persuader] Perfect! So then you are familiar that they are an outreach program that helps children not only from different countries but also in the U.S. get the help that they need?
 [Persuadee] Yes, they are a great help to all. I am very impressed with them.
 [Persuader] That's so comforting to hear! Not many people are aware of the organization! They have many ways that we can help continue their mission. Are you familiar with any of those programs as well?
 [Persuadee] I only know about the feeding program. I did not know they did other things
 [Persuader] Yes, the feeding program is probably the most common and also one of the most successful. However they do have other programs as well that helps keep them moving. You can become a monthly donor, sponsor a child, shop the gift catalog from their website, or there's the Make a one-time gift program, which is what I'm here for!
 [Persuadee] How much can they really do with a couple of bucks though?
 [Persuader] They can feed entire camps with several couple dollars! That's how they're funded! They get running water and electricity to children that need it. Just a few bucks adds up when its coming from a couple of people, you know?
 [Persuadee] I guess so. Seems they have many supporters, makes me feel like mine drop in the bucket is meaningless.
 [Persuader] I don't think so at all. It makes you a contributor to a wonderful cause, not a drop in a bucket! If a few bucks was the difference between getting child(ren) out of a hostile living environment and into one more stable, wouldn't that mean something to you? That definitely could be the case. It's not meaningless. It's a valued contribution.
 [Persuadee] I would possibly donate at some point
 [Persuader] That's great to hear and you have the perfect opportunity right now. 
 [Persuadee] I want to be able to give more than $2. I will consider giving in the future. 
 [Persuader] You could give the $2 from chatting with me about this cause and donate again - by any one of those means that I mentioned above in any amount that you are satisfied with. It's free money going to a good cause and it all gets taken care of directly from here. 
 [Persuadee] I prefer to give directly through the website. I am here to make money.
 [Persuader] That's so unfortunate. It's basically giving free money to children who have no essentially nothing and you're still getting paid whether you donate or not. 
 [Persuadee] I understand where you are coming from, I just prefer to give on my own time.
```
</details>

### 11. `20180831-221232_645_live`  —  old modifier: `conditional`

**Why:** Declines the in-task donation, preferring to research and give independently: "having to research the charity myself - seems like the better option." No task-payment commitment is ever made.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello it's important to save the children and it most important charity. do you agree
 [Persuadee] I don't know that I'd say it's the most IMPORTANT charity, but it is an important one, yes.
 [Persuader] children are future and saving them should be priority
 [Persuadee] Okay, so how do we make them a priority?
 [Persuader] if children doesn't have a future no country can progress
 [Persuadee] Okay, and how do you plan to help to give children a future?
 [Persuader] i think we should donate some money for this cause
 [Persuadee] Can you tell me anything about this cause? What is their mission? What do they do? Who do they help (besides children)? Where are these children they're helping?
 [Persuader] the have a website URL 
 [Persuadee] But you specifically are the one asking me to donate?
 [Persuader] yes if you agree they same you donate I can donate also and it will be from task money
 [Persuadee] but you can't tell me anything about the cause...that doesn't make me feel like what you're saying is truthful as in you're going to match my donation
 [Persuader] this money goes for a cause one example is millions of Syrian children have grown up facing the daily threat of violence. In the first two months of 2018 alone, 1,000 children were reportedly killed or injured in intensifying violence
 [Persuadee] Question, is it just for oversea's children?
 [Persuader] no children in need all over the world. It's US based website please see
 [Persuadee] You as a "spokesperson
 [Persuader] if you are interested we both can donate some money out of our task money
 [Persuadee] I think I am interested in donating directly through the website that you directed me to - I'm not sure if you are aware, but they have several means of donating. 
 [Persuader] that's fine. it's up to you
 [Persuadee] Unfortunately, having to research the charity myself - seems like the better option. But, you are right it is a good cause and if you are serious I hope you still donate.
```
</details>

### 12. `20180723-062856_180_live`  —  old modifier: `deferred`

**Why:** Final line is an explicit hedge: "okay, I might donate." No amount is ever committed.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi, do you usually donate to charities
[Persuadee] I DO
[Persuader] great! You're such a nice person. What charities do you usually donate to?
[Persuadee] To church, I return tithes and I also do the offerings
[Persuader] great! Well, have you ever heard about Save the Children charity?
[Persuadee] no, can you tell me more about it?
[Persuader] it's an international non-governemntal organization that promotes children's rights, provides relief and helps support children in developing countries
[Persuadee] nice! I have a child so i'm all about helping kids
[Persuader] would you donate to this charity? your donation will make such a huge impact for some children
[Persuadee] I would like to know more before i donate. How do i know if it's a legit organization
[Persuader] it is a trustable fund! It's one of the top rated charities in the world!
[Persuadee] interesting. So if i donate will 100% of my donation go to a child?
[Persuader] 86% goes to help children, 9% goes to fundraising and 5% goes to management and other things. 
[Persuadee] i just don't know why i've never heard about it
[Persuader] neither do i! It's such a well known charity! It just so sad to see children from developing countries die from easily preventable deseases
[Persuadee] it is sad, i agree with you 
[Persuader] million of Syrian children have grown up facing the daily threat of violence. You said you have a kid. Imagine your precious child going through it every day. waking up every day being afraid of getting killed
[Persuadee] that breaks my heart. I would do anything to protect my son
[Persuader] And you can also protect those children if you donate to our fund! YOU can make a difference
[Persuadee] okay, I might donate
[Persuader] Great! How much would you like to donate? You're awesome
```
</details>

### 13. `20180723-072435_196_live`  —  old modifier: `deferred`

**Why:** Final line: "i'm not sure. I'm in a tough financial situation right now so i really need money but i would like to donate." Explicitly unresolved, no amount given.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hey, how are you doing?
[Persuadee] Hi, i'm doing great! how are you?
[Persuader] Doing ok here. Glad to hear your day is great. Do you have a moment to talk about children causes?
[Persuadee] sure! I would like to
[Persuader] Have you ever heard of the charity, Save the Children?
[Persuadee] no, but i would like to know more about it
[Persuader] Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries.
[Persuadee] that's great. Do you have any more information about it?
[Persuader] Yea. Have you heard of children getting separated from their family at the US-Mexico border?
[Persuadee] yes, it's so heartbreaking1
[Persuader] Save the Children are helping to reunite them with their family.
[Persuadee] that's really good to hear! I can't imagine not being able to see my son! 
[Persuader] Children shouldn't be separated from their families. It is very heartbreaking to hear, and I'm glad Save the Children stepped in.
[Persuadee] So what exactly do they do to help these kids to reunite with their parents?
[Persuader] They identify the parents who were deported back to their countries of origin, while their children remain separated and detained in the U.S. As these parents are identified, they work to help them locate and safely reunite with their children, and from there, support them in getting access to essential services they need to re-establish themselves.
[Persuadee] awesome! I'm so gonna support it! Children should be with their parents!!
[Persuader] Would you like to help and donate to them? Your donation will be directly deducted from your task payment. You can choose any amount from $0.50 to all your payment.
[Persuadee] I can't donate less than 0.50?
[Persuader] Sure. What amount would you feel comfortable donating?
[Persuadee] i'm not sure. I'm in a tough financial situation right now so i really need money but i would like to donate.
```
</details>

### 14. `20180723-093434_153_live`  —  old modifier: `deferred`

**Why:** Intent to donate is stated ("i will definitely donate then") but the dialogue cuts off mid-negotiation over the exact amount ("I don't think I can do 5$" / minimum is $1) with no final figure confirmed by the Persuadee.

<details><summary>Full dialogue text</summary>

```
[Persuader] hey
[Persuadee] hey there, how are you?
[Persuader] im good hru
[Persuadee] i'm doing great. It's a lovely day today
[Persuader] Yes, I am so glad the sky is clear over here today.
[Persuadee] great. So i'm here to talk about some children's charity. Can you tell me the name of this charity?
[Persuader] Yes, The Save the  Children Charity organization is an extraordinary effort to provide assisstance to children in developing countries. Would you like to learn more about how you could make an impact with a small donation?
[Persuadee] yes sure, i would like to know more
[Persuader] Save the Children is an internationally trusted chairty that strives to make an impact to serve individual children and their family gain basic access to resources needed to survive. The organization has many credentials afforded to them , including the World Health Organization.
[Persuadee] Sounds great to me! how much can i donate?
[Persuader] Thank you for your sincere concern for the health of our children around the world. Any amount truly helps, from $1 to $100 or more. Thank you so much again for helping our organizations efforts.
[Persuadee] I'm still debating on how much i want to donate
[Persuader] Well, my first donation to Save the Children was only $2 if you want a reference.
[Persuadee] okay, i will consider that. would you mind telling me something else about this organization
[Persuader] No problem! Save the Children is responsible for helping innocent children's welfare in deadly war zones, and the recent lack of support has made a lot of children go starving nights, for days even weeks. 
[Persuadee] that's so sad. Do you know if they help Syrian children?
[Persuader] Yes! We help all children around the world. The  recent lack of support has been very disheartening, and has had us in the need
[Persuadee] ok, i will definitely donate then
[Persuader] Thank you so much for your help. Would you like to make a special $5 donation that will go to help costs of providing food to our Syrian committee
[Persuadee] I don't think I can do 5$ 
[Persuader] That is perfectly fine, whatever amount is comfortable for you. $1 is the minimum donation
```
</details>

### 15. `20180723-094242_630_live`  —  old modifier: `deferred`

**Why:** No amount or commitment is stated by the Persuadee anywhere in the dialogue; it stays a general discussion about charity.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi, how are you today?
[Persuadee] I am okay. How are you?
[Persuader] i'm doing great! I'm working for Save The Children organisation, have you heard about it?
[Persuadee] No, I haven't. Can you tell me more about it?
[Persuader] sure. Save the Children is an international NGO that promotes children's rights and provides relief and helps support children in developing countries
[Persuadee] What types of programs does it offer?
[Persuader] they ensure children's rights to health ,education and safety. They are currently helping Syrian children
[Persuadee] On my side I don't have information about the task, only that we are trying to come up with a donation agreement. Are you looking for a donation for the charity?
[Persuader] yes, You can donate as little as 1 cent and as much as 2 dollars. your donation will be directly deducted from your task payment
[Persuadee] Okay, that is good to know. What types of things are being done to help the children in Syria?
[Persuader] 1000 children were killed or injured and the donations can address these problems. Our organization gives shelter to those kids, feed them and take care of them
[Persuadee] Do you know what percentage of donations goes directly to programs (as opposed to overhead costs, salaries, and expenses)?
[Persuader] yes, 86% of all the donations goes to programs and the rest goes to maintaining the fund, ads, etc
[Persuadee] That sounds pretty good. What other countries are they working in right now?
[Persuader] They are actually helping children at the US Mexican border to reunite with their parents
[Persuadee] What inspired you to work for Save the Children?
[Persuader] I have a son and I can't imagine seeing him hungry or in pain or afraid of being killed. i want to help all the children in the world
[Persuadee] That's an honorable reason. :) What is the one thing you would say to someone to encourage a donation?
[Persuader] a couple of cents or a couple of dollars might not make a difference in your life but it can make a huge impact on some child's life
[Persuadee] That is a good way to think about it. And every little bit can add up.
```
</details>

### 16. `20180723-103902_895_live`  —  old modifier: `deferred`

**Why:** Final line: "I would consider donating $0.50" - explicit hedge ("would consider"), never firmed up.

<details><summary>Full dialogue text</summary>

```
[Persuader] Save the children is a good organization. Do you like to donate to charities?
[Persuadee] Yes, I do. What does Save the Children do?
[Persuader] he Save the Children Fund, commonly known as Save the Children, is an international non-governmental organisation that promotes children's rights, provides relief and helps support children in developing countries.
[Persuadee] Can you give me their website, so I can look into them?
[Persuader] Sure, here is the link.  URL 
[Persuadee] Thank you! Why are you talking about this charity instead of the others?
[Persuader] Sure, here is the link  URL 
[Persuadee] Why are you talking about this charity instead of the others?
[Persuader] I think it is a charity that is well deserving and underfunded. Children in underdeveloped countries do not have the support that other kids have and I just want to give them a chance to improve their lives. 
[Persuadee] In what ways do they help children? 
[Persuader] They provide things such as food and medical treatment. Things that are basic needs are given to them. 
[Persuadee] I\'m glad they do that but there are many charities that "claim" to do the same thing.
[Persuader] Yes, you are correct. However, this organization has been effective in helping others and all donations are matched. I believe their goal is to really help the children. They are known to help in disasters too. 
[Persuadee] Well, ok. I'll keep them in mind and do some research into them.
[Persuader] Do you think you would like to donate in future?
[Persuadee] If I can vouch for them, yes.
[Persuader] That is great. I hope you consider them and decide they are worthy
[Persuadee] I'm glad there are people like you out there who are attempting to make a difference in the world. 
[Persuader] Thank you. If you had a chance to donate some of your money earned today, how much would you donate to the charity now? Your donation would be directly deducted from your task payment. You can choose any amount from O dollars to all your payment. 
[Persuadee] I would consider donating $0.50.
[Persuader] Wow. That is wonderful. You are a really generous and caring person.
```
</details>

### 17. `20180825-043229_970_live`  —  old modifier: `deferred`

**Why:** Firm $20 now ("I'll make a $20 donation today") plus a separate hedge about future increases ("If it checks out like you say, then I'll consider upping any future donations") - matches the firm-now-plus-hedge-about-more-later pattern.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello how are  you doing today?
[Persuadee] I'm good, how are you?
[Persuader] I am well.   Just enjoying the sunny day and trying to help out a charity I am working on, Save the Children.
[Persuadee] I wish I had some sun. Please tell me more about this charity
[Persuader] This charity is n international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries. I have recently donated some money to it.   Would you be interested in how much I donated?
[Persuadee] Yes please. And also, was the donation mandatory or voluntary?
[Persuader] I donate about $15 a month and it is all voluntary.  I rather put my money into this charity then church offering because I know it directly helps children.  Would you like to know how I know it helps?
[Persuadee] That sounds like a reasonable amount. Sure, tell me more about how it's used
[Persuader] A year ago, I saw kid begging on the street who look really hungry.   I was about to give him some money until a representative for "Save the Children" walked ahead of me and help this kid out.   This person took them to their facility and provided food, shelter, and clothing.   A month later I saw the kid was healthier, happy, and cleaner.  I was so impress I decided to make a donation.   Would you be interested in a donation?
[Persuadee] Wow. Nice story. I'm very particular about who I donate to so I'd need more information
[Persuader] Understand.   
[Persuadee] About how many people a month does the charity help?
[Persuader] Since it is international it helps more then 1000's of kids per month.
[Persuadee] And is there a minimum amount required per month (like on of those sponsor a kid charities) or can it be just a one time donation?
[Persuader] No minimum, can be a one time donation.
[Persuadee] That sounds doable. Do you know by any chance if this is a registered charity? I want to make sure not all the money is going to the staff via salaries
[Persuader] Its non-governmental but is register to for tax purposes.   Only about 25% goes to the management/staff of the charity.
[Persuadee] Okay, that's good to know. I'll make a $20 donation today and keep researching this charity. If it checks out like you say, then I'll consider upping any future donations
[Persuader] This is great.  Thank you for your donation. 
[Persuadee] No problem. Thank you for telling me about the charity. Have a great day
```
</details>

### 18. `20180826-023807_40_live`  —  old modifier: `deferred`

**Why:** No specific amount is ever confirmed; final line is a musing about a $5 latte and "ways to set up recurring donations," not a stated pledge.

<details><summary>Full dialogue text</summary>

```
[Persuader] Did you Know that Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries.
[Persuadee] I think I've heard of them, but aren't they religiously affiliated? I'm all for improving conditions for children in developing countries, but I don't really want money paying for evangelizing.
[Persuader] Yes they are affiliated with religion but all proceeds are put towards saving the children they do profit are use any funds for personal gain or spread of religion.
[Persuadee] How transparent are they about uses of their funds? Are they well rated by the watchdog groups that keep an eye on non-profits?
[Persuader] Save the Children is. Mention the organization's credentials and international impact
[Persuadee] It's great to hear there are people out there doing such important work. Have you ever donated to them?
[Persuader] Yes I have , how much do you spend on unnecessary stuff like a bag of snack or candy. You Know small donations can help a lot of children and their families
[Persuadee] Really? I suppose even with the economy being as hard as it is, exchange rates are still good enough to make a real impact. 
[Persuader] Yes any donations made to helpless children make a real impact on their life. Not many kids get a real shot and they all deserve one If I had a chance to change a childs life foe the better and didn't I would not be able to live with myself.
[Persuadee] That's a good point, I think a lot of the times the little things we can do that have really positive impacts kind of get lost in the shuffle. If I can ask a personal question, how did you make room in your finances to donate?  
[Persuader] I did't I just gave what I thougt cas right and took the blow . I thought about how these kids do without so much and realized I could do without once in order to help someone in need
[Persuadee] So how did you decide what was right for you? 
[Persuader] I gave what was given to me . Over the next few chats I'm going to tell you the story of Bruce a child that like alot of these chidren need help but threw Save The Chidren found it. At the end Of our next few chats I'm going to ask you to  donate what you earn from this survey . I want you to think about what it means to save a child thats in trouble and how by saving that child you find new hope in your own life.
[Persuadee] I'm certainly willing to listen. Tell me about Bruce.
[Persuader] Bruce was born to a single mother who was only 14 at the time he came into this world , the girls mother and father were ashamed of her pregnancy and kicked out of the house. Bruce was born and taken from the girl because she was to young to raise him and her was adobted out to a poor family that did their best to provide for him . The founder of save the children heard about the family and learned of Bruces story . He came to meet Bruce .
[Persuadee] That poor girl, being rejected by her own family like that. I'm glad that Bruce was taken in, though. How did the visit go?
[Persuader] The owner got involved in Bruces life and sav the children went to work and provide food and cloths and school needs for Bruce . Bruce went own to join the save the children foundation after he completed college and is helping save children today. 
[Persuadee] That's awesome! He even made it through college. I can see how he'd be really devoted to the organization, given the impact they had on his life.
[Persuader] Yes he is a force for good and was saved out of tragedy.
[Persuadee] If only all kids were so lucky. But I guess it takes a lot of work to try to help the ones who need it most
[Persuader] Now I would Like to ask you to donate what you about to receive and and give to other in need. Yiur will go to help other just like that right now are looking or in room by themselves hoping for a miracle .Will you be that miracle and help a child like Bruce today? 
[Persuadee] I will. Be the change you want to see in the world, right?
[Persuader] Yes you will . So how much of your earnings will you give, for a child that needs to be saved today?.
[Persuadee] 5 dollars buys a latte, and I think it should be easy for me to give up a coffee a month. I bet they have ways to set up recurring donations pretty easily.
[Persuader] Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment. The research team will collect all donations and send it to Save the Children
```
</details>

### 19. `20180826-040651_411_live`  —  old modifier: `deferred`

**Why:** Ends unresolved with garbled phrasing ("my donation comes from my other payment") and the Persuader's final question about the task payment goes unanswered.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello, how are you today?
[Persuadee] hello i am fine thank you
[Persuader] Have you heard of our charity Save the Children?
[Persuadee] yes I've donated $ 150 to this year for this organization
[Persuader] Awesome, you know all about it then!
[Persuadee] I know more or less how it works and my goals are, but what do you know
[Persuader] I know it is an international non-governmental organization that promotes children's rights while also providing relief and support for children in developing countries. It is awesome there are people that dedicate their lives to help ensure children have the rights to health, education, safety, and much more.
[Persuadee] very fair, it is good that all contribute little to the help of children all over the world
[Persuader] This is very true. So how do you feel about donating today?
[Persuadee] I feel the happiest man in the world when I donate some help if she is, I feel very good when my help is happening to people
[Persuader] This is great to hear, not everybody feels that way!
[Persuadee] I do not only help the children but everybody who needs some help if this financial or moral help
[Persuader] It sounds like we need more people like you in the world.
[Persuadee] true, we live a life and it would be more fun to live beautifully and happily but not only for ourselves but to be happy for all the people who surround us somewhat
[Persuader] This is true. Everybody deserves the option to be happy. We all should have equal opportunity to be happy and succeed in life.
[Persuadee] if I define what makes me happy in life is to look and my beloved happy man
[Persuader] That is an awesome definition. So seeing as how you mentioned you would like to donate today, what is a specific amount you would be willing to donate?
[Persuadee] I wanted to buy clothes for myself today, but I will give them some kind of charity online search, full $ 100
[Persuader] That is great to hear, however. Your donation will be directly deducted from your task payment. You can choose any amount from 0$ to all of your payment.
[Persuadee] work here is the other thing, my donation comes from my other payment
[Persuader] That's awesome, so you'd like to donate all of your task payment?
```
</details>

### 20. `20180826-044626_167_live`  —  old modifier: `deferred`

**Why:** Persuadee proposes $0.25 ("yes I can donate... How about .25?") but the Persuader pushes back for more ($25) and the dialogue ends without a final agreed figure.

<details><summary>Full dialogue text</summary>

```
[Persuader] Morning! Have you considered donating to Save the Children? It's a great organization and doesn't cost much to help a child in need.
[Persuadee] I have not. I am not sure I know what Save the Children is. 
[Persuader] It's an  international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries. It has done wonderful things and is a big part of many organizations employee giving drives.
[Persuadee] Oh cool. Do they help people here in the USA?
[Persuader] Right now they're concentrating at an international level. Did you know that in the first two months of 2018, over 1,000 children were reportedly killed or injured in Syria alone? They also appeal to stop hunger issues abroad.
[Persuadee] Yes, I know about Syria. I know hunger is a big issue for a lot of people in other countries. Do they provide food for these people?
[Persuader] They provide whatever is needed. AND, in relation to the US, they are currently working on the Hurricane Lane situation in Hawaii. They are also big on sending girls to schools in other countries.
[Persuadee] Sounds like they do a lot of different things for people. 
[Persuader] Yes. it's a great organization. You can find out more if you'd like. I can give you their website. How much would you be willing to donate?
[Persuadee] I am not sure yet. What is their website?
[Persuader]  URL  Any amount of would be appreciated. They can do a lot of things with your donation.
[Persuadee] I will look at the website. Is the donation tax deductible? 
[Persuader] Depending on tax laws in your state, it is. You may need to check with your tax advisor. How about donating to sponsor a child in the US?
[Persuadee] Do I get anything for donating? 
[Persuader] Other than the satisfaction of helping a child in need?!  You will receive a photo with the child you sponsor and can correspond with them if you choose.  How much would you like to donate?
[Persuadee] The photo would be nice, it would let me know and connect with someone I am helping. How do I know my money goes to the cause and not just to the pockets of the people that run it.
[Persuader] This is a great organization with a very stellar reputation. There are FAQs on the website that can address all of those concerns, which I certainly can understand. How about a donation of $25 to start?
[Persuadee] How long has Save the Children been helping people all over the world?
[Persuader] It varies for different regions of the world. Would you be willing to start your donation today, while we're talking?
[Persuadee] yes I can donate. I don't have much. How about .25?
[Persuader] If you think $.25 will get a child fed, we can do that. However, I think $25 would be more beneficial and it would go to so many good causes.
```
</details>

### 21. `20180826-061949_863_live`  —  old modifier: `deferred`

**Why:** Final line contains an explicit hedge: "I'll look into the website and likely donate $5."

<details><summary>Full dialogue text</summary>

```
[Persuader] Do you know about Save the Children?
[Persuadee] I have not heard of this charity before! Have you?
[Persuader] I have.I actually a  monthly donor
[Persuadee] That's great! Would you mind explaining what the charity does?
[Persuader] The charity collects donation from people like you and me and help children in need
[Persuadee] Sounds like quite the worthy cause. Are the children in need all across the world? Or just the United States?
[Persuader] all over the world.I saw a children died from hunger and it tears my heart apart.I decide to be part of the solution since then
[Persuadee] Wow, that is extremely sad. It is extremely unfortunate that child hunger is so prevalent in this world. 
[Persuader] Save the Children organization is a blessing to the world.They have been helping children,finding houses and food.
[Persuadee] It really sounds like a blessing! What is their website? I'd like to learn more information.
[Persuader]  URL Specially in countries at war children are helpless.
[Persuadee] Great, thank you! Is there a monetary goal set for the year?
[Persuader] NO.It is not.You can donate as much as you want
[Persuadee] That is amazing. 
[Persuader] How much money do you spend on candies that can be helping children in need?
[Persuadee] I do not purchase candy too often; however, I could definitely sacrifice a Starbucks Coffee to help children in need.
[Persuader] Please do that.Children need your help
[Persuadee] Yes, most definitely. Thanks for making me aware of this charity!
[Persuader] How much do you like to donate today?
[Persuadee] I'll look into the website and likely donate $5.
```
</details>

### 22. `20180826-062736_188_live`  —  old modifier: `deferred`

**Why:** No specific amount is ever stated anywhere in the dialogue. Final line ("Yes I would") responds to the Persuader's "consider making a donation!" and most naturally reads as agreeing to consider it, not a firm pledge.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi there! Can I tell you all
[Persuadee] Hello how are
[Persuader] sorry it cut me off...can I tell you about a charity called Save the Children?
[Persuadee] Yes pleas do
[Persuader] They help children make sure they have access to health resources, education, and safe environments.
[Persuadee] Sounds like a good charity. What countries do they provide service to?
[Persuader] mainly children in developing countries.  Did you know over 1,000 children were killed in Syria in just the first 2 months of 2018.
[Persuadee] What kind of health benefits to they provide to the children?
[Persuader] they provide them access to doctors and medicine that they wouldnt normally get.  Donations are their main source of income.
[Persuadee] What is the standard monthly donation someone usually gives.
[Persuader] A lot of people like to give 30/month so it's only a dollar a day.  however any donation helps, even just 1 dollar.
[Persuadee] What percentage of my donation actually makes it to the children?
[Persuader] 86% goes towards the services...the rest is used mainly for fundraising efforts
[Persuadee] Could you provide a breakdown of where that 14% goes?
[Persuader] 9% fundraising and 5% goes towards keeping the charity running like salaries etc
[Persuadee] Is save the children backed by any religious organizations?
[Persuader] I'm not sure about religious organizations but several large companies partner with them.  Would you consider making a donation?
[Persuadee] Could you pleas give examples of the large companies?
[Persuader] Google, Disney, target and paypal
[Persuadee] What percentage of your total donations come from these large corporations.
[Persuader] Most come from individuals like you.  consider making a donation!
[Persuadee] Yes I would
```
</details>

### 23. `20180826-065245_39_live`  —  old modifier: `deferred`

**Why:** Explicit hedge: "I probably will do that." No firm resolution follows; conversation moves on to unrelated pleasantries.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello there, how are you doing today?
[Persuadee] I'm great, thanks. How are you?
[Persuader] I'm doing swell, thanks for asking! So how do you feel about children?
[Persuadee] I love children. I believe they are our future and should be taken care of in the best possible way.
[Persuader] That's great! I happen to agree! Do you have any children yourself, or do you plan to in the future?
[Persuadee] I do not have children of my own and am not able to have them. I am contemplating adoption for the future.
[Persuader] Oh, that's wonderful! So many kids out there need a home, after all! There are so many issues today with children, all over the world! For instance, did you know that in the first two months of 2018 alone, over 1k children were killed or injured in intensifying violence?
[Persuadee] Wow, that is a staggering amount. I did not know that. I am a big fan of organizations who take care of the needs of hurt children.
[Persuader] Oh? That\'s awesome! I assume you\'ve heard about the organization called "Save the Children" then?
[Persuadee] I have! They seem to be doing a good job.
[Persuader] That, they do! Did you know they've won over 7 different awards for their charitable work? As a former foster kid, it makes me happy to see this place bring such awareness to the issues and needs of our young. 
[Persuadee] I am not surprised to hear that at all. Children should not have to do through so much tragedy and devastation at such young ages. It is great that others are looking out for them.
[Persuader] Absolutely! In fact, you can even help! If you want to make a small donation from your task payment, I'm sure it would be greatly appreciated! You can donate just a few cents, or even the whole amount of your final payout if you choose!
[Persuadee] I probably will do that. If everyone did something, it helps the bigger overall picture and they are so worth it.
[Persuader] Absolutely! I mean, we already spend money on small snacks or a coffee we could forgo, why not give it to a charitable cause? How noble of you!
[Persuadee] I just know that if I were a child in need, I would be grateful for all the help I could get.
[Persuader] Absolutely! I remember being in a group home as a kid, and a bunch of ladies had made blankets and hats for us. I still have the blanket I was made to this day! A little goes a long way :)
[Persuadee] Wow, that is so good to hear. I'm sure it is not easy for organizations to get charitable work done but I am grateful they try and that others get involved. Kuddos to them!
[Persuader] Yeah, it really is humbling to watch society ban together and help each other! Either way, I'm sure Save the Children will appreciate your donation, and be able to save many more children in the future. You have a good day!
[Persuadee] The life of a child is always worth saving. You have a good day as well.
```
</details>

### 24. `20180826-070323_186_live`  —  old modifier: `deferred`

**Why:** Ends unresolved: "I'm not sure! What is the range of options?" No amount is ever given.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi! How are you doing today?
[Persuadee] Good, thanks! How are you?
[Persuader] I am doing well thank you. Do you ever donate to charity?
[Persuadee] In the past few years I rarely have.
[Persuader] I know, it can be hard to donate. especially in today's society, but a tiny amount, even less than a dollar, can go a long way
[Persuadee] That seems so hard to believe, but I guess lots of pennies still add up!
[Persuader] Exactly, I feel the same way sometimes, but think if everyone in the US gave a nickel, that's over 16 million dollars
[Persuadee] Wow, that definitely puts it in perspective! 
[Persuader] There are so many charities too, but I believe that children are the future, and we need to do what we can to help them have fulfilling lives
[Persuadee] I agree with you! 
[Persuader] Have you ever volunteered? It's another way to help without having to spend any money
[Persuadee] I have! I used to volunteer often, but I have so little time it feels like now!
[Persuader] Time and money these days can be scarce! But think about the little things you buy, and maybe one week, instead of buying that bad of chips or cup of coffee, donate it to the children
[Persuadee] You're right! It doesn't take much sacrifice to think of small ways to help!
[Persuader] And think of all the kiddies you will be helping!
[Persuadee] Haha that's true!
[Persuader] do you think you will donate today?
[Persuadee] I think so!
[Persuader] How much would you like to donate?
[Persuadee] I'm not sure! What is the range of options?
```
</details>

### 25. `20180826-082717_200_live`  —  old modifier: `deferred`

**Why:** Only ever says "I would be interested in making a donation" (a hedge) and "ok that sounds great" (vague); no amount is ever committed, and the dialogue trails off into unrelated small talk.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello, would you be willing to donate some of your money to save the children?
[Persuadee] To save the children where?
[Persuader] It is a non-governmental organization that helps children in developing countries
[Persuadee] What does it help the children with?
[Persuader] With their rights and relief for many daily necessities like food, water, shelter, and education to name a few
[Persuadee] Is there a minimum donation?
[Persuader] A minimum donation of 10 cents would be appreciated, which is a third of the money received for this task. The more the better.
[Persuadee] I would be interested in making a donation
[Persuader] Thank you so much. Your donation will be directly deducted from your task payment.
[Persuadee] ok that sounds great
[Persuader] Okay. Thanks. Is there an option on your end where you can donate?
[Persuadee] No there is not
[Persuader] So how do we finish this conversatin then?
[Persuadee] I have no idea, maybe after we have 10 chat turns each
[Persuader] Lol, I guess we have to chat a few more turns. 
[Persuadee] where are you from?
[Persuader] Originally from Romania, but I live in the US in California. How about you?
[Persuadee] I am born and raised in Florida
[Persuader] Nice, would like to travel and visit other states sometime when Im free.
[Persuadee] I made $100+ everyday last week on Mturk and now all I have left is these low paying surveys
```
</details>

### 26. `20180826-181717_640_live`  —  old modifier: `deferred`

**Why:** Only ever discusses donating personal time ("I will donate two hours of my time") to a different, unnamed charity of their own choosing outside this task - no money commitment to this task's charity is ever made.

<details><summary>Full dialogue text</summary>

```
[Persuader] hii
[Persuadee] Hello how are you?
[Persuader] good are you going to make a donation
[Persuadee] I am definitely thinking about it! How about you?
[Persuader] I am I'm going to donate 5 dollars
[Persuadee] 5 dollars is a good amount! How much time do you think 5 dollars would be if I wanted to donate time?
[Persuader] I'm not to sure honestly
[Persuadee] What would you ballpark?
[Persuader] I don't understand
[Persuadee] Could you take a guess on how much t ime
[Persuader] maybe 2 hour's
[Persuadee] 2 hours would be good. I will donate two hours of my time then.
[Persuader] that's a great idea
[Persuadee] What charity are you going to donate to?
[Persuader] save the children
[Persuadee] save the children is a great one!
[Persuader] yeah and you
[Persuadee] I would like to find one that has a focus on childhood cancer
[Persuader] that's really good
[Persuadee] Thank you! Just want to keep the children healthy and safe
```
</details>

### 27. `20180826-182048_519_live`  —  old modifier: `deferred`

**Why:** Never resolves past hedges: "I would want to research them first" and "maybe we could both donate to them." No firm commitment is made.

<details><summary>Full dialogue text</summary>

```
[Persuader] hello
[Persuadee] Hi, I currently have a children's charity that I sponsor
[Persuader] ok tell me 
[Persuadee] We sponsor a child in El Salvador, we have been going it a number of years.
[Persuader] Thats great. 
[Persuadee] How about you do you have a favorite charity?
[Persuader] I donate money to save the children
[Persuadee] what do you know about them are they a good charity?
[Persuader] Yes. Save the children is a great charity. They are really serious about helping children.
[Persuadee] I see - how many years have you been with them
[Persuader] I have been donating money to save the children for 5 years. I give them 1000 dollars every year. 
[Persuadee] that is a good approach, i have been doing some research on charities
[Persuader] You can donate any amount to save the children. Would you like to donate a dollar or more to them?
[Persuadee] well that would be a good but I would want to research them first to make sure they are good but maybe you have already done that
[Persuader] I have done my research and I can tell you they are a great organization full of kind / sincere people.
[Persuadee] that's great maybe we could both donate to them
[Persuader] Yes that is a great idea. Would you like the link to their website?
[Persuadee] sure can you send it to me
[Persuader]  URL    - Have a great day.
[Persuadee] thank you  for sharing it ...you as well
[Persuader] Thank you for your time.
```
</details>

### 28. `20180826-182054_411_live`  —  old modifier: `deferred`

**Why:** Devolves into a political tangent; the one relevant line ("I will have to take a look and send in my donation!") is itself a deferral to a later independent action, and the dialogue never returns to confirm anything.

<details><summary>Full dialogue text</summary>

```
[Persuader] Children are our future, we need to do our best to ensure them grow up well. The torch of life pass on.
[Persuadee] I agree completely, if we don't take care of our future and our present our society won't have a future. People these days donate to mediocre things, I really think there should be a bigger focus on children's charity's. Personally I have met so many families who have benefited from the Ronald McDonald charity. They are provided everything that the family needs so they are able to stay close to their children. 
[Persuader] How to ensure our children grow well and live well?  Our clean water, clean air and world peace, all of us connected someway. Our endless needs and wishes put our children in danger. Life really needs not much.  
[Persuadee] I think focusing on our needs as a whole community vs. just ourselves or our families is a great first step. There are so many families that are well off, and know what meal they are to have next, but they don't contribute to those who don't. This is why I donate each month. To help insure that other families in my community are provided with their basic needs. 
[Persuader] Scientists put American way of life, if the whole world lives like American, it needs 7 earths. That is why there are endless fighting, we need to look at what happen to Syrian children, the Middle East.  Its fighting never end, for cheap oil? for weapon testing? 
[Persuadee] The American way of life, isn't perfect by any means. You have so many people that have way too much, and other who's children are starving and go without basic necessities. By being divided and realizing that there are issues all over the world, is what is making matters worse. We are forgetting our children, forgetting their needs, their wants, and their right to live out the life they deserve. They are getting lost in the shuffle of things. 
[Persuader] The top 1% own the world and they do not share, they want our children join the army fight for their interests, protect their interest. The capitalism took over the government. Our penny donation really can not change the root of the problem since we do not have to start. We need to take our government back to work for its people, the whole world's people and share! 
[Persuadee] We can't expect the independently wealthy to understand and work for the interests of the poor. So I feel like it is our duty to donate, raise money, and work to help those around us. 
[Persuader] https://support. URL ite/SPageNavigator/sponsorship.html#!/  I wish I could help everyone of the kids here.
[Persuadee] I will have to take a look and send in my donation! 
[Persuader] Thank you so much! Also we need to realize just one government police change could save millions. 
[Persuadee] What do you think the change is? That is needed from the government police. 
[Persuader] Policy, sorry.  Government is so important for people. 
[Persuadee] I don't understand why we can't all just get on the same page? What is the need for war? It's just boys playing army, and the children will be the ones to suffer when they are long gone. 
[Persuader] Harvard Med graduate Don Berwick was pediatrician most of his life, only when he worked for Obama for 11 months, he found out all his life was saving children, not worth a policy change.
[Persuadee] I never knew that! 
[Persuader] Republic did not confirm him, so he came back to MA. They also want small government, so on one protect they could rob more from the weak around the world. 
[Persuadee] The top 1% can only be the top 1% if everyone else stays poor. 
[Persuader] The top 1% is control the world wealth, so they control the governments around the world. The poor countries treat them like god, the rich country lost jobs and everything else.  
[Persuadee] And unfortunatly many of the charities are run by the 1% as well. The redcross is the biggest example of this. 
[Persuader] At the mean time, we could only done our best donate and help what we can.  URL
```
</details>

### 29. `20180827-044233_823_live`  —  old modifier: `deferred`

**Why:** Firm $0.10 today plus a separate hedge about more later: "I can only do $0.10 today, though... hopefully more in the future." Matches the firm-now-plus-hedge-about-more-later pattern.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi, have you ever made a donation to a charity before
[Persuadee] Hello.  Yes, occasionally.
[Persuader] The Save the Children foundation is essential to help ensuring children's rights to health, education, safety, etc. 
[Persuadee] Okay.  What types of things do they help with?
[Persuader] Since 1932, Save the Children has been on the ground providing support to the most isolated and underserved children in rural America. From our earliest days in Appalachia _ helping children and families hardest-hit by the Great Depression _ to today, our U.S. team goes where others cannot.
[Persuadee] That's good work.  What about other countries?
[Persuader] Save the Children is the voice for vulnerable children. We're on the ground in 120 countries, working to reach every last child through international programs that focus on health, education, protection and disaster relief. 
[Persuadee] That's wonderful.  Sounds like a good charity.  
[Persuader] They also play a part in disaster relief.No one knows when the next earthquake, flood or tsunami will strike. But we do know children are severely affected by natural disasters. They also suffer greatly during conflict, drought and disease outbreaks. Save the Children's natural disaster response and emergency relief programs help protect vulnerable boys and girls during disasters and their aftermath.
[Persuadee] That's very important.  A natural disaster can be devastating, even as an adult.   I imagine critical for children. 
[Persuader] so what do you think, would you be interested in making a donation
[Persuadee] Sure, I'd be willing to make a donation.  I'm kinda broke right now, so it'll be a small amount.  I can do $0.10 today, and hopefully more in the future. 
[Persuader] How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment.
[Persuadee] I like donating to worthy causes when I can.  It sounds like Save the Children are doing good work.  I can only do $0.10 today, though.  I'm hoping even though it's a small amount, if many people do it, it can add up to more. 
[Persuader] your donation is kind and will be out to good use
[Persuadee] That's good to know.  
[Persuader] The save the children foundation will put this donation to good use
[Persuadee] Great!   That makes me happy.
[Persuader] Thank you again for your generous donation.
[Persuadee] You're welcome.   Thank you for advocating for the charity.
```
</details>

### 30. `20180827-050719_208_live`  —  old modifier: `deferred`

**Why:** Same pattern: "I can give $0.05, and hopefully more in the future."

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi there. How are you today?
[Persuadee] I'm well, thanks for asking. 
[Persuader] Did you know you can donate some or all of your earnings to Save the Children today?
[Persuadee] I did think that may be possible.   Can you tell me more about Save the Children?
[Persuader] It is an organization that helps kids in other countries who may not have food and water. I can hardly imagine what that would be like. I am blessed to have 3 healthy children here in America.
[Persuadee] That's great!  Every child should have the same opportunities in life, but unfortunately that doesn't happen.  What are some of the things Save the Children does to help?
[Persuader] They make sure these kids have clean water to drink as well as food and they have access to medical care.
[Persuadee] Nice.   Are they the ones that make those commercials?  The ones that show kids in bad situations?  That commercial makes me so sad!
[Persuader] Yes they are. They make me sad to. But also reminds me how much I have and how blessed I am. I have so much more then they do. I would want to help them out. Even just a few cents would help them. Don't your think?
[Persuadee] Me too.  Yes, I think it's a great cause.  I like to think that if a bunch of people give just a little, it can add up to do a lot of good.  I can give $0.05, and hopefully more in the future. 
[Persuader] Awesome! Thank you for helping them. I will be doing the same thing.
[Persuadee] Great!   Thanks for advocating.  I hope you have a great day!
[Persuader] Have a wonderful day.
[Persuadee] We need 10 turns, so here it is.  Thanks for your time.
[Persuader] Okay. It was fun chatting with you! 
[Persuadee] you too.  I think it's interesting and creative for them to be doing this on mturk, don't you think?
[Persuader] Yes I do. How long have you been doing mturk?
[Persuadee] I did it a bunch in 2014 when I was unemployed.  I'm doing it now because I'm broke until I get my first paycheck from a new job I'm starting tomorrow.   You?
[Persuader] I do it when I'm bored. And I put the money away for vacation or retirement. I enjoy it.
[Persuadee] I don't enjoy it that much, only out of necessity.  That's quite responsible of you!
```
</details>

### 31. `20180827-060832_308_live`  —  old modifier: `deferred`

**Why:** Final, resolved position is an explicit deferral: "I plan to donate next month" - outside this task.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi how are you today?
[Persuadee] ya fine you
[Persuader] do you donate to charities?
[Persuadee] No I will not donate. but i plan to donate
[Persuader] Thats great. Do you volunteer?
[Persuadee] yes. you heard about that charity
[Persuader] save the children. It is an amazing charity
[Persuadee] Are You Already donate to charity?
[Persuader] I do donate when I can, yes
[Persuadee] ok very nice 
[Persuader] yes, i try to make ends meet, but a few cents can go a long way
[Persuadee] how much to donate
[Persuader] I try to do a couple hundred a year
[Persuadee] oh great best of luck
[Persuader] yes, thank you. How much do you donate?
[Persuadee] i will donate to 10$
[Persuader] that is very generous!
[Persuadee] how much you donate
[Persuader] I will donate 10 too
[Persuadee] I plan to donate next month
```
</details>

### 32. `20180828-151016_679_live`  —  old modifier: `deferred`

**Why:** Only commitment language is hedged and self-contradictory: "I will probably do that for sure." No amount is ever stated.

<details><summary>Full dialogue text</summary>

```
[Persuader] Do you feel like the children of the world should be better looked out for?
 [Persuadee] Yes I do. I believe there are lots of vulnerable and helpless children everywhere who deserve a lot more than they are getting.
 [Persuader] Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries. Have you heard of them before?
 [Persuadee] Yes, I have heard of them before and it has all been good things. I like organizations who take care of our children.
 [Persuader] Save the Children believe no child should go to bed hungry and it's their goal to make this a reality.
 [Persuadee] That is a very noble goal and I hope that lot's of people get behind them so they can continue to do what they are doing.
 [Persuader] How can this world have so many wealth people but yet have so many people who are suffering! Do you feel like those who are well off should do more to help? Doesn't it upset you when they don't?
 [Persuadee] Well I don't think the amount of wealth has much to do with it. I think it has to do with what is in people's hearts. Whether you are rich or poor, it all comes down to whether you are a giving person.
 [Persuader] Exactly! I could never turn a blind eye to those who are in need. How about you?
 [Persuadee] I agree completely. I give to all sorts of non profit organizations and charities whenever I can. I just imagine that if I am ever in need that I would want someone to help me.
 [Persuader] In the first two months of 2018 alone, 1,000 children were reportedly killed or injured in Syria. Insane numbers right!?!?
 [Persuadee] That is really sad! What was the cause of that? War?
 [Persuader] It is a civil war between those in power and those who feel the need to fight back for a better life.
 [Persuadee] So basically they are harming the ones who would one be their future leaders and the ones taking care of them.
 [Persuader] It's a despicable mes i tell you! Would you be willing to donate something to help them? our donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2).
 [Persuadee] I will probably do that for sure. Every little bit helps and if everyone does something, it will make the load a little lighter.
 [Persuader] The research team will collect all donations and send it to Save the Children. I'm going to give some of my earnings as well.
 [Persuadee] That is great to hear. Who knows the impact that they will make over the course of time.
 [Persuader] I wish more people would open up their hearts and try to help the way you did.
 [Persuadee] Well I'm sure there are lots out there who would if they could.
```
</details>

### 33. `20180829-144704_720_live`  —  old modifier: `deferred`

**Why:** Firm $1 already agreed ("I think a dollar is enough" / Persuader accepts), but the Persuadee's actual final statement adds a separate hedge about the future: "I'll donate more in the future" when less broke. Matches the firm-now-plus-hedge-about-more-later pattern.

<details><summary>Full dialogue text</summary>

```
[Persuader] How much would you donate to the children's charity?
[Persuadee] how about a dollar?
[Persuader] Every dollar counts for the charity to help the childrens. Do you think you can donate a bit more?
[Persuadee] Well, I figured i would at least keep a dollar to myself
[Persuader] I understand but these are children, it would help them out very much. Every dollar counts.
[Persuadee] I think a dollar is enough.
[Persuader] Ok, if you say you'll donate a dollar that will be fine. I'm really glad you decided to donate.
[Persuadee] No problem.  
[Persuader] The research team will collect all donations and send it to Save the Children, so thank you!
[Persuadee] awesome, no problem.  Good luck.
[Persuader] And good luck.
[Persuadee] How do I end the chat?
[Persuader] I think we need to do atleast 10 inputs, the one before I counted 7.
[Persuadee] Oh crap. okay.  This is tough since we've already reached an agreement lol.
[Persuader] Well I guess there's a few more information I forgot to mention. (2 more input to go).
[Persuadee] Okay, what else is there?
[Persuader] I forgot to link the website to Save the Children  URL 
[Persuadee] Alright, I'll check it out.
[Persuader] Sounds good I hope the website helps out.
[Persuadee] i think when i have some more money, and I'm not so broke, I'll donate more in the future.
```
</details>

### 34. `20180830-204841_559_live`  —  old modifier: `deferred`

**Why:** Final line literally contains "if": "I would donate $2 if that is the payment for the task." Borderline - the condition (confirming the payment is $2) is true per the Persuader's earlier message, so this reads more like a factual clarification than genuine hesitation, but per the strict "any if" rule and the guideline's own "when in doubt, no" instruction, flagging as OK rather than overriding. Worth a second look.

<details><summary>Full dialogue text</summary>

```
[Persuader] hi
[Persuadee] Hi to you too
[Persuader] so have you heard about Save the Children before?
[Persuadee] Yes I have heard about it but don't know much about it
[Persuader] Well it's a global non-profit charity based around helping children.
[Persuadee] What are the donations mostly used for
[Persuader] They are used for helping children in a variety of areas: access to education, healthcare, protection from abuse, and relief from natural disasters or conflicts.
[Persuadee] How are donations solicited ?
[Persuader] Well you can go on their website  URL  or it can be deducted from this task payment.
[Persuadee] When finished with this  task  I will be sure to check the website.
[Persuader] It's definitely worth a look, plenty of useful data and more information on how they operate.  Are you interested in donating?
[Persuadee] How does donating from my  task payment  work ?
[Persuader] Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2) after the chat.
[Persuadee] I will do that but At what point do I make the decision ?
[Persuader] After the chat is concluded, the window will move on, and you can input an option.
[Persuadee] How does the chat come to an end?
[Persuader] After about 10 turns.  Do you have any idea what you'd like to donate?
[Persuadee] I would donate $2 if that is the  payment for the task
[Persuader] Well that's good to hear, and if you respond that should lead you to the next page.  It was a pleasure to talk to you :)
[Persuadee] Same here, although I do not see the reason to tie a chat to the donation request.
```
</details>

### 35. `20180831-040908_90_live`  —  old modifier: `deferred`

**Why:** Firm $1 repeatedly reaffirmed ("okay don't worry I will donate"), but paired with an explicit hedge/question about additional future giving: "I will donate today but is it possible I donate later too?" Matches the firm-now-plus-hedge-about-more-later pattern.

<details><summary>Full dialogue text</summary>

```
[Persuader] Good Friday morning to you! How are you today?
 [Persuadee] Hello, I am fine, how about you?
 [Persuader] I am doing really well. I am a little surprised at how cold it is here this morning-it's only in the 50's, which I was not expecting. How is it by you?
 [Persuadee] It is warm here. Are you interested in donating? 
 [Persuader] Interesting. I was going to ask you if you had heard about the organization Save the Children. Are you interested in donating even $0.05 of today's pay to help the kids?
 [Persuadee] I am very interested in donating, I have a soft heart for children and I will donate as much as possible
 [Persuader] Well that is really great. What is the amount you would like to pledge from today's payment?
 [Persuadee] I guess i will help $1, is this an international charity?
 [Persuader] That would be a great help to the children! Thank you! Yes this is a charity that not only helps outside of the US but also inside. Have you heard about the storms/flooding in Hawaii?
 [Persuadee] I have not heard. in how many countries do they work? and which issues they work on mainly?
 [Persuader] STC works to provide kids with the basic things that they need like food, healthcare and shelter issues. I know as soon as the floods hit Hawaii STC pledged to help out. The US based center is in CT. Are you interested in more info?
 [Persuadee] Yes I am. I will donate today but is it possible I donate later too?
 [Persuader] Yes, you can donate any time. I have you down for $1 for today, right?
 [Persuadee] okay don't worry I will donate. I just want to know more about it. is there any big company cooperating with them? 
 [Persuader] I can give you their website. It is URL let me know if the link comes through.
 [Persuadee] okay I will explore it, thank you. I like to know more
 [Persuader] Well, from what I read, close to 90% of the money that they collect goes directly to the kids. I know that makes me feel really good. How about you?.
 [Persuadee] It makes me feel good too. I like it if they are so clear with their financial reports
 [Persuader] Yes. Did you see that they also give the chance to sign up and sponsor individual kids? Also, thank you for your $ donation!
 [Persuadee] Yes I've seen it and there are many big companies working with them, like IKEA and Disney
```
</details>

### 36. `20180831-180851_529_live`  —  old modifier: `deferred`

**Why:** Ends in an outright refusal: "No, I never donate." No commitment is ever made.

<details><summary>Full dialogue text</summary>

```
[Persuader] Would you be interested in donating some of your payment to the charity Save the Children?
 [Persuadee] I am not sure. What on Earth is Save the Children? Is it some sort of boy band?
 [Persuader] Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries.
 [Persuadee] Hm. Isn't this the sort of group that the government should help?
 [Persuader] Everything helps, and honestly they could use it more than we could. Children die of hunger everyday and your donation could help prevent that.
 [Persuadee] At the moment, I'm pretty strapped for cash. In fact, I could probably use a donation!
 [Persuader] Well, you could donate anything from $0.01 to $2.00. Would you be willing to donate even $0.01?
 [Persuadee] What would be the point of donating such a small amount? It would be better to try to find others that could donate more.
 [Persuader] No amount is too little unless it is nothing. Save the Children is a well established charity, so they have a large reach and it all adds up. You can check them out at their website: URL 
 [Persuadee] Where does StC do its work? I've never heard of StC. Is this a real org?
 [Persuader] They are a global charity, they also work in the US. You can check out their website, it is indeed a reputable organization. 
 [Persuadee] Have you ever made a donation to them? Or has anyone that you know made a donation? 
 [Persuader] I have not, but in this instance I wouldn't mind donating. It is just a bonus.
 [Persuadee] I understand that the organization needs money, like many other worthy charities trying to improve the world. But right now, it's a bit tough for me. I know that you understand.
 [Persuader] Well, we will just sit here going back and forth and then neither of us get the bonus? I assure you that even a penny would help.
 [Persuadee] Would you be willing to donate yourself?
 [Persuader] Yes, of course. For all we know this is theoretical money.
 [Persuadee] How much would you be willing to donate?
 [Persuader] I usually do half because I feel it is fair and these organizations could use it more than I could. Anything below a dollar I would consider donating. Do you ever donate to things in your personal life?
 [Persuadee] No, I never donate. I don't know what organizations do with the money, how efficient they are.
 [Persuader] Yeah I understand that.
```
</details>

### 37. `20180831-191711_71_live`  —  old modifier: `deferred`

**Why:** Dialogue is cut off exactly at the Persuader's amount question; no reply or figure from the Persuadee is ever given.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello. My name is Jae. And who am I speaking with on this fine day?
 [Persuadee] HI my name is Gail. How are you?
 [Persuader] Well hello Gail. I am very fine. Thank You for asking. I truly appreciate that. And how is your day today, Gail?
 [Persuadee] It's great. I made turkey burgers for dinner. Do you like to cook?
 [Persuader] WHAT??!! I just had left over turkey. Mmmmmmmmmm. Turkey sounds great. Sounds much better than my version of turkey. And yes, I like to cook. Do you have any leftover turkey burgers? lol
 [Persuadee] I actually do! lol. You should come over and try some! lol. I like spicy food, so I used jalapenos too.
 [Persuader] OMG, Gail!!!! You're a woman after my own heart. Where have you been? ,)
 [Persuadee] LOl I've been in Texas! We love to grill. Where are you from?
 [Persuader] I always wanted to visit the "BIG" state. Definitely have to go down south very soon. As for me, I\'m in the BIG Apple, NYC. And speaking of burgers and spicy food, do you share your expertise in these fine foods with charity or charity work?
 [Persuadee] I used to cook for the local church sometimes.I prepare meals for those in needs.
 [Persuader] Awesome, Gail. That is great work indeed. Well, the reason why I ask is because I represent a great organization called, "Save the Children". We are an international non-governmental organization that promotes children\'s rights, provides relief and helps support children in developing countries and we are looking for donations today. Gail, I need your burgers..............excuse me, your charity in a well to do donation. Can I interest you in this?
 [Persuadee] Sure, I wouldn't mind helping.
 [Persuader] Awesome!!!! Gail, as soon we started this conversation, I felt great things about you. The vibe was right. Besides the great charity work at your church establishment, have you done any other types of charity before?
 [Persuadee] Yes, I like helping where I can.
 [Persuader] Gail, you are a SAINT!!!! We need more angels like you, especially in today's climate of change. Gail, your provided donation today will essentially help in ensuring children of the world rights to health, education, safety, and most of all, safety. You will make a tangible impact for the world. Would you like some examples, statistics as to why we fight the good fight?
 [Persuadee] Yes, I like giving back. I usually work through college organizations or a church.
 [Persuader] In histories past to today, we are shown the lack of support for children in developing countries, especially in war torn areas. For instance, millions of Syrian children have grown up facing the daily threat of violence. In the first two months of 2018 alone, 1,000 children were reportedly killed or injured in intensifying violence. Your donation can address such problems. Gail, my angel. You are part of the solution. Let me ask you, how much money do they spend on unnecessary stuff like a bag of snacks or candy?
 [Persuadee] I would say five dollars.
 [Persuader] Well, that five dollars can be used in more meaningful ways now. Your small donations will indeed help a lot of children and their families. Gail, shall we get started with your donation then?
 [Persuadee] Yes, of course.
 [Persuader] You are amazing, Gail!!!! How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2).
```
</details>

### 38. `20180831-211837_377_live`  —  old modifier: `deferred`

**Why:** Only says "I would like to donate" (soft, no amount) and ends on "How do I donate?" - never resolves to a specific commitment.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi...
 [Persuadee] Hello
 [Persuader] Do you know about children charity?
 [Persuadee] I can't say I'm terribly familiar.
 [Persuader] Sorry, I do not understand what you say
 [Persuadee] I am saying that I do not know what children charity is or what it implies
 [Persuader] Have you donate any charity?
 [Persuadee] Yes, specifically to a charity for cancer research
 [Persuader] Okay, Do not you know about Save the children?
 [Persuadee] No I do not
 [Persuader] The Save the Children Fund, commonly known as Save the Children, that promotes children's rights, provides relief and helps support children in developing countries.
 [Persuadee] I see. Thanks for the explanation
 [Persuader] Do you like to donate the Children charity?
 [Persuadee] How much do people usually donate at a time
 [Persuader] Sorry, I do not know that.
 [Persuadee] I would like to donate
 [Persuader] Oh! That is great. Thank you very much.
 [Persuadee] How would the process go?
 [Persuader] I'm not fully aware of this, but I've donated it
 [Persuadee] How do I donate?
```
</details>

### 39. `20180903-053722_705_live`  —  old modifier: `deferred`

**Why:** Hedged throughout: "I may donate a few cents" ... final line "Maybe I can do some more" - no firm figure ever confirmed.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi there! How are you doing today?
[Persuadee] I am doing alright, thanks, and yourself?
[Persuader] Doing well thank you. 
[Persuadee] What are we here today for?
[Persuader] We are here today to discuss the children's charity Save The Children.  Have you heard of it? 
[Persuadee] i have heard a little bit
[Persuader] Are there causes you believe in and donate to in efforts to support their mission?
[Persuadee] i volunteer and donate for a charity that works with children of abuse
[Persuader] Interesting.  What are your thoughts in supporting children who suffer in other ways throughout the world? Save the children helps all children who're hardest to reach and  are in vulnerable situations 
[Persuadee] That is great. I would definitely want to look into. 
[Persuader] You can find more information at  URL  I was hoping you would consider donating today. 
[Persuadee] I try to donate when I can, but I am currently broke. It's hard to part with the littl money I have
[Persuader] If you decided to donate today, your donation will be directly deducted from your task payment. You can choose any amount. Personally I intend on donating all my proceeds from this task. For a few minutes of work and having the ability to donate even a small amount that will make a difference is easy. With that said how much do you like to donate to the charity now?
[Persuadee] I may donate a few cents
[Persuader] A few cents is great!  Any bit helps and at the end of the day thes children are in need.  Save the children works with 120 countries so even a small bit can help. 
[Persuadee] Do you donate often?
[Persuader] I do. I intend on donating the full amountoday. For just a few moments of my effort I know that th
[Persuadee] that is great that you donate
[Persuader] Yes. I realize how fortunate I am even with the little I have. My understanding is $2 can go along way with these children. I can spend a bit longer working and have satisfaction that made a difference today. I thank you for considering to donate. Perhaps you could add a bit more than a few cents to create a bigger impact on these children's lives. 
[Persuadee] Maybe I can do some more
```
</details>

### 40. `20180903-103939_512_live`  —  old modifier: `deferred`

**Why:** Amount is walked back under pressure (from $0.25 down to an apparent $0.15) and the final line explicitly hedges about the future: "maybe more next time." (Note: OCR/text quality on this line is poor.)

<details><summary>Full dialogue text</summary>

```
[Persuader] Save the Children is a great charity you should consider donating to
[Persuadee] yeah , i agree it is a great charity, but i prefer to donate to St Jude
[Persuader] I think that's great too but if you already give to St Jude why not give to Save the Children this time?
[Persuadee] I guess I could throw them .10
[Persuader] Why not give them more so they can really help the children with it?
[Persuadee] I am so broke but giving a dime is really all i can afford today.
[Persuader] It wouldn't hurt to give more. Honestly, if you think you're broke you should see how poor these children are. You know they're worse off than you, right?
[Persuadee] Honestly < do not think so. My dqaughter and I are Homeless at the moment and have to sleep in parking lots.. To be able to afford to get her some milk would be nice.
[Persuader] These are kids we're talking about they know nothing but war going on and you already mentioned you give to St Jude. Why not give what you were going to give to St Jude to Save the Children?
[Persuadee] 0k Here is a .25
[Persuader] Couldn't you split it 50/50? Give them $1? I mean you'd give that to St Jude wouldn't you?
[Persuadee] I would ifd my daughter was not needing milk also... Its hard to donate when I feel i would be taking from my daughter to give to other children.. 
[Persuader] This isn\'t money you\'ve even seen yet though. It\'s "imaginary" money until it materializes so that\'s different? I\'m sure you could give $2
[Persuadee] Its not imaginary money though... what i give takes away from ours later.
[Persuader] Well think of all the money you spend on things you don't need? $2 is definitely money we waste daily and that would really help these kids.
[Persuadee] No, I do not waste any money, Right now school is about to start and she has no school supplys or anything new for school. shoot i am the biggest tight wad when it comes to trying to save anything for her.
[Persuader] Then why not give some money to these kids too? They have even less than your daughter has. You can surely spare $2
[Persuadee] no, I cant .25 is the most I am willing to part with.
[Persuader] How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2).
[Persuadee] >15 cents sorry maybe more next time.
```
</details>

### 41. `20180903-104450_565_live`  —  old modifier: `deferred`

**Why:** Firm 30 cents plus a separate hedge about more later: "I can probably give more later." Matches the firm-now-plus-hedge pattern.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello!
[Persuadee] Hi!
[Persuader] Have you ever heard of Save the Children?
[Persuadee] I think I may have.  You can tell me about them.
[Persuader] The first thing I want to share with you is that Save the Children is an international non-governmental organization that promotes children's rights. They help children all over the world. 
[Persuadee] That sounds like an important cause.
[Persuader] It is very important. You and I are part of the solution though. It's our moral responsibility to help. How much would you like to donate now? 
[Persuadee] I may be interested but first can you tell me what my donations go to.
[Persuader] Sure. Right now millions of Syrian children have grown up facing violence every day. Your donation helps to address those problems. 
[Persuadee] Do you donate to this organization personally? 
[Persuader] Yes, I just donated a couple of days ago. I am so fortunate that my family has their needs met. I turn to tears when I see children suffering. 
[Persuadee] How long have you been apart of this organization?
[Persuader] I don't work for them. I only communicate through this platform to help them.
[Persuadee] Ok it really sounds worthwhile.  I am always willing to help kids.
[Persuader] Thank you. How much would you like to donate? You know whatever amount you choose, the donation will be directly deducted from your task payment.
[Persuadee] What is the average of what most people donate?
[Persuader] You can choose any amount from ten cents to two dollars today. 
[Persuadee] Ok today I think I can do thirty cents.  I can probably give more later. 
[Persuader] Thank you. The research team will collect all donations and send it to Save The Children. I'm sure I'm going to donate more today also. It's such a good cause.
[Persuadee] Thank you for telling me about this worthwhile cause!
[Persuader] You are welcome. Have a nice day.
```
</details>

### 42. `20180903-131723_996_live`  —  old modifier: `deferred`

**Why:** Firm 20 cents plus a separate hedge about more later: "After I think about it, I may donate more." Matches the firm-now-plus-hedge pattern.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello. How are you doing today?
[Persuadee] Hi. I'm doing well on this holiday.
[Persuader] I'm very glad to hear that. Can I ask if you are someone who is interested in charitable organizations?
[Persuadee] Most likely. I have given to different local organizations regularly.
[Persuader] That is very good to hear and I thank you for helping others. Have you ever donated to the organization Save the Children?
[Persuadee] I've heard of them, maybe from television commercials. 
[Persuader] Do you know much about what they do?
[Persuadee] Not really. Can you tell me more?
[Persuader] I would be happy to. Save the Children works nationally and internationally to help children. They promote children's rights, provide relief, and support children in developing countries. 
[Persuadee] So Save the Children does help children in the United States as well as around the world? 
[Persuader] That is correct. And people can be sure that their money is being well spent when they donate because 86% of all expenditures go to program services.  
[Persuadee] Oh, ok. That's good to know since there are way too many charities that don't. 
[Persuader] Yes, unfortunately some charities use more than the should to pay high salaries for CEO's. Please also be aware that Save the Children even does work in countries like war torn Syria where 1,000 children were injured or killed in the first 2 months of 2018 alone. 
[Persuadee] I think I'm interested but how would I donate from here?
[Persuader] You can go to their website directly anytime. You can also donate now if you would like. How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2).
[Persuadee] I think I will donate 20 cents today. After I think about it, I may donate more.
[Persuader] I and the organization very much appreciate it. The funds will be put to good use. They do a lot of good work here and in developing countries where needs are extreme. 
[Persuadee] So do I just wait and see if my donation is automatically taken?
[Persuader] You will be asked shortly how much you would like to donate. And if you would ever like to donate in the future, please visit the website. Thank you again for your contribution. 
[Persuadee] Alright. Thanks for the information.
```
</details>

### 43. `20180903-170041_976_live`  —  old modifier: `deferred`

**Why:** Explicitly declines to donate now in favor of a larger donation later: "I was actually thinking of keeping this bonus and sending a percentage of my payout at the end of the week." A textbook deferral.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hey! How are you doing today?
[Persuadee] I am doing great how are you doing?
[Persuader] I'm not doing too bad. It's been a good long weekend!
[Persuadee] Agreed! our newborn has been pretty grumpy the last couple days
[Persuader] Well congratulations on your newborn!
[Persuadee] Thank you she is a beautiful little girl. Even during her grumpy days I would not trade her for anything. 
[Persuader] That's lovely, you can never get those grumpy days back.
[Persuadee] Nope and they are usually paired with the good days. 
[Persuader] Yeah, you have to take the good with the bad.
[Persuadee] Absolutely. Is there something we are supposed to be discussing in particular?
[Persuader] Have you ever heard of the charity Save The Children?
[Persuadee] I actually have. I have made contributions to them before. Actually just last week I sent $20 donation to them!
[Persuader] Nice! They're a very good organization that are trying to make a difference in children's lives in developing countries.
[Persuadee] Yes they are! And with the new daughter I understand the need more than ever.
[Persuader] Would you like to donate any part of your task payment to Save The Children today?
[Persuadee] I was actually thinking of keeping this bonus and sending a percentage of my payout at the end of the week. that way I can give them a larger donation. 
[Persuader] That's understandable. Any bit helps and that's a mighty thing for you to do.
[Persuadee] Thank you! Have you donated to any organization like this before?
[Persuader] I have. I donate to them every chance I get to do this hit, and I work at a Children's Hospital and I donate there as well.
[Persuadee] That is truly amazing!
```
</details>

### 44. `20180904-024226_703_live`  —  old modifier: `deferred`

**Why:** Hedge persists to the end: "I think I can spare a penny" plus an explicit conditional about more later ("If I have a chance to donate when I'm a bit more financially stable, I will donate more").

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi, how are you today?
 [Persuadee] I am fine. And you?
 [Persuader] Not too bad :) Have you heard of Save The Children?
 [Persuadee] I have, actually.
 [Persuader] They do greeat work at least I think what about you?
 [Persuadee] I'm often skeptical of big charities like that. They sometimes don't put the money that is donated into the right projects.
 [Persuader] I know normally I am too but I was convinced to research them once by a very giving friend and I found that they do a lot of awesome work and a big majority if not all donations go back into the charity and lining someones pocket
 [Persuadee] I have just done some quick research and am inclined to donate when I have the opportunity. If a charity is doing good work to feed the hungry, I will give what I have to spare.
 [Persuader] hehe, I meant rather then lining someones pocket....So do I have your commitment to donating some today at the end of the HIT?
 [Persuadee] I don't really have anything to give right now, but I will donate at another time when I have steady income.
 [Persuader] They give you an option at the end of the HIT to donate even 0.01 would be very helpful....a penny couldn't hurt could it?
 [Persuadee] I suppose not. I mean, a penny is nothing in the grand scheme of things. If I have a chance to donate when I'm a bit more financially stable, I will donate more. Right now, I think I can spare a penny. :)
 [Persuader] Good, and I'll match and times it by five and now we'll have donated 0.06
 [Persuadee] Alright. Will the penny be taken from my mturk account? That would be the most convenient thing for me.
 [Persuader] yes, it'l be taken from your bonus and you won't even notice it missing to be honest.... good karma.... maybe you'll be lucky today ;)
 [Persuadee] Well, thank you for wishing me well. May your days be pleasant, as well.
 [Persuader] how's the weather?
 [Persuadee] Warm and rainy here.
 [Persuader] it's warm but not rainy that I know of
 [Persuadee] Hurricane season is upon us, so I'm keeping a really close eye on that.
```
</details>

## Part B — Reverted back to `yes` (37)

Every dialogue below ends on what reads, on manual re-read, as a clean, unhedged, resolved commitment to a specific amount (or 100%/half/etc. of task payment). The old annotator's `conditional`/`deferred` tag was most likely triggered by earlier hesitation in the same conversation that later got resolved. **These 37 have been changed back to `yes` in both dataset files.**

### 1. `20180826-174957_757_live`  —  old modifier: `conditional`

**Why:** Persuadee's stated precondition ("Not without knowing the exact organization") is satisfied when the Persuader supplies the URL. Final line: "I will donate 20 cents" - no hedge remains once the condition is met.

<details><summary>Full dialogue text</summary>

```
[Persuader] I think out of all charities saving the children is most important one as children make the future. Hope you agree
[Persuadee] I definitely agree
[Persuader] this is good as you agree with opinion as everyone should do the same
[Persuadee] Yes - providing funding for children is a top priority, whatever the need may be
[Persuader] I usually put some money for this cause yearly
[Persuadee] What kind of children's charities do you think are the most important?
[Persuader] I think children below the poverty line is most important
[Persuadee] Yes - someone needs to be looking out for those children! I say, if you have enough than give to others
[Persuader] basic education is very important to have a good future
[Persuadee] Important to make sure their basic needs are met too -- food, clothing and shelter
[Persuader] what is the good amout you think
[Persuadee] It depends, should this be a monthly donation or annual?
[Persuader] annually one time payment
[Persuadee] Ok, sounds good. I think a range between $100 - $250 would be appropriate
[Persuader] would you like to donate something from your task payment for this cause
[Persuadee] Not without knowing the exact organization
[Persuader]  URL   Also I will donate the same amount whatever you decide
[Persuadee] I am unclear as to whether or not this is a real donation or just discussion for the sake of the task
[Persuader] Whatever you want to donate from your task money
[Persuadee] I will donate 20 cents
[Persuader] thanks will do the same
```
</details>

### 2. `20180831-184520_110_live`  —  old modifier: `conditional`

**Why:** Persuadee's stated precondition (wants a website before committing) is satisfied when the Persuader supplies the link. Final line: "Oh wonderful, thank you I will donate 0.75 of my payment for sure." No hedge remains.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello
 [Persuadee] Hello there how are you today?
 [Persuader] I am good. How are you?
 [Persuadee] I am doing well myself, thanks.
 [Persuader] I was wondering would you like to donate money to Save the Children?
 [Persuadee] Could you tell me more about it?
 [Persuader] You can donate as little or as much as you want. It is to help children in need all over the world.
 [Persuadee] I am guessing this a charity?
 [Persuader] Yes. I'm Sorry. it is for charity. I thought I mentioned that.
 [Persuadee] No, its fine! This is a non-profit charity, not government sponsored?
 [Persuader] It is a Non-Profit Charity
 [Persuadee] I would be interested in donating a portion, how would that work?
 [Persuader] We have a few options. You can send in either a check or money order. Make a donation on our website or have a monthly payment deducted from your banking account.
 [Persuadee] Oh I see, is there a website I can look at or a number I can call before I make that kind of commitment?
 [Persuader] Yes there is
 [Persuadee] Ok, I am interested in helping refugees from Syria especially children so I would like to see if they are working on helping them
 [Persuader] Absolutely, I totally understand.
 [Persuadee] Could you tell me the website address?
 [Persuader] Here is the website http:// URL 
 [Persuadee] Oh wonderful, thank you I will donate 0.75 of my payment for sure.
```
</details>

### 3. `20180723-042226_724_live`  —  old modifier: `deferred`

**Why:** Final line: "Thank you, I will do it for sure, have a nice day" - said in direct response to the Persuader explaining the end-of-task donation popup. "For sure" carries no hedge; this is the same-task completion mechanic, not an outside-task deferral.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi there. How are you today?
[Persuadee] Hello, I am fine, how about you?
[Persuader] Very well thanks. Do you currently give any money to charity on a regular basis?
[Persuadee] Yes, I try to help time to time
[Persuader] Any charity in particular?
[Persuadee] No, anything that catches my eyes, or I find them on gofundme, what about you?
[Persuader] I have a few payments set up monthly. I assume then you've heard of Save the Children and the great work they do with young people?
[Persuadee] Yes, I've heard of it. Can you please explain more about it?
[Persuader] Firstly, they provide funds and support services to help protect vulnerable children all over the world. Once the children have a safe environment the next priority is to improve their lives via education and other resources. They really make a difference to the lives of children in poverty or destitution.
[Persuadee] I am interested in it. I already checked their website. Health and education both are important factors
[Persuader] Absolutely. And the great thing for us is that even a very small donation goes a long way due to the number of people who can donate! We're asking people today to give a small part of the payment for this HIT to the charity. You'll get a box pop up at teh end of our chat which will give you the opportunity to donate something. Obviously the more the better, but I also appreciate that you aren't turking for free so you can judge it yourself.
[Persuadee] Actually I like these kind of HITs. I did few HITs before that asked me to donate my bonus or half of the reward. I happily did. I am sure there are people who need it more than me
[Persuader] You're absolutely right-  sometimes we don't realise it, but what seems like a little bit of moeny to us can make a big difference to them. I worked in Africa earlier this year and the difference a few dollars can make to people over there is unbelievable.
[Persuadee] Yes, few dollars can save a child or can help a family to survive for a month. How long have you worked there?
[Persuader] I'm back in the UK now - I was in South Africa (Durban) for three months from January to end of March for work.
[Persuadee] That is so nice of you. It is a big thing to do. Thinking about starving children makes me so sad. I wish I could do more
[Persuader] We can all do something - donate a little bit or volunteer to try to help. There are lots of opportunities
[Persuadee] Yes you are right, I help as much as I can. at least I try. "save the children" sounds like an amazing organization. They work in 120 countries already
[Persuader] They certainly do and tehy are well established so you cna be certain they are going to use the money in a good way.
[Persuadee] Yes It looks like a trustworthy organization with no doubt. I already read few of their reports on their website. I wish they can help even more countries
[Persuader] Me too. When we click done that donation box will appear - it should be pretty self-explanatory. I hope you enjoy the rest of your day. Thanks again.
[Persuadee] Thank you, I will do it for sure, have a nice day
```
</details>

### 4. `20180723-075339_567_live`  —  old modifier: `deferred`

**Why:** "i'll donate 20 cents" is stated plainly mid-dialogue with no hedge word anywhere, and nothing afterward retracts or qualifies it. No deferral language found anywhere in this dialogue.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi, how are you today?
[Persuadee] hello! pretty good, you?
[Persuader] i'm doing great! I'm helping Save the Children Charity to raise money. would you like to know more about this wonderful fund?
[Persuadee] yes please! i was just looking for a charity to donate to
[Persuader] This wonderful charity helps suport children in developing countries!
[Persuadee] what do they support exactly? education?
[Persuader] they promote children's rights, provide relief. They are currently helping children at the US Mexican border to reunite with their families and they also help Syrian kids
[Persuadee] ok thats great. i would like to donate but i dont have a lot of money myself. is $20 okay?
[Persuader] So you can't donate 20$. The way it works is you can donate your whole payment of 2$ for this task or you can donate as little as a couple of cents
[Persuadee] i'll donate 20 cents
[Persuader] that's very generous and it will help tremendously!  in the first months of 2018 1000 children were killed or injured in intensifying violence and your donation can help to address this problem
[Persuadee] i'm happy with that. i'd donate more but i don't have much myself
[Persuader] i understand. as i said even a couple of cents would help! You're the part of the solution!
[Persuadee] thanks! i'm glad to help
[Persuader] This organisation is so wonderful! 86% of donations are going for a cause and the rest goes to management of the fund 
[Persuadee] that's amazing! i love that so much of it goes towards the children
[Persuader] yes! Isn't it wonderful! 
[Persuadee] it definitely is!
[Persuader] I'm glad there are people like you in the world who are willing to help
[Persuadee] i like to help since people have helped me
```
</details>

### 5. `20180723-091419_371_live`  —  old modifier: `deferred`

**Why:** Ends: "So you'd like to donate?!" / "Yes, I would :)" / ... / "Oh yeah, absolutely!!" - an enthusiastic, unhedged yes. No conditional/deferred language appears anywhere in the dialogue.

<details><summary>Full dialogue text</summary>

```
[Persuader] Have you ever heard of Save the Children?
[Persuadee] I haven't!
[Persuader] It's basically what it sounds like
[Persuadee] What kind of situations do they work with?
[Persuader] The organization helps children around the world with life, protecting them, coming to their aid when a crisis arises, helping them when necessary. 
[Persuadee] That sounds like an awesome organization! Do you know how someone can get involved? 
[Persuader] They have a website. You can also make a .50 cent donation through me from your compensation of this hit. The donation will go towards food and/or aiding them with their health.
[Persuadee] That's simple enough. I like the sound of that! Have you ever personally worked with them?
[Persuader] I have made donations in the past, yes. It made me feel good to know that I could provide some type of help especially because I have children of my own. The research team will collect all donations and send it to Save the Children.
[Persuadee] Gotcha! I also have a child, so I understand where you're coming from. I have a soft spot for children in general. 
[Persuader] Same! Especially less fortunate children.
[Persuadee] Absolutely! I always think about how I would want to know my child is cared for if I'm not around. It's definitely a motivator! 
[Persuader] I agree. This is one of my favorite organizations to donate to and they're well known and have done so much for children all over.
[Persuadee] That's good to know that they're reputable. Sometimes I'm cautious of donating, just because I want to know that they're making the difference that they saw they are.  
[Persuader] At least here we know the researchers are making the donations through this hit.
[Persuadee] It is nice to know that!
[Persuader] So you'd like to donate?!
[Persuadee] Yes, I would :)
[Persuader] Awesome! Thank you so much :)
[Persuadee] Oh yeah, absolutely!!
```
</details>

### 6. `20180723-093509_578_live`  —  old modifier: `deferred`

**Why:** Final line: "as per today's earning is very little I would like to donate 1" - a specific, resolved amount ($1) stated as the answer to the Persuader's direct amount question, immediately followed by the Persuader confirming the deduction mechanism.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi! Have you ever heard of Save the Children? It's a charity!
[Persuadee] yes I do
[Persuader] What do you think of it?
[Persuadee] well, it is a charity work / organisation where they save many children 
[Persuader] Yup! And it's an international group, and not owned/sponsored by any government.
[Persuadee] you're right, it is non-profit organisation. 
[Persuader] Have you ever considered donating to them?
[Persuadee] it is an NGO, yes ofcourse many times I have considered to donate them as per my ability 
[Persuader] Me too. And I just learned today that they have partnerships that match individual donation - so every amount a person givves is actually doubled. Did you know that?
[Persuadee] aw, really ? No I haven't heard of it 
[Persuader] Yes, I was really surprised too. And I learned that they focus on health first, but also prioritze education. I think that is important, as it will help the children grow up with a better chance of being successful. What do you think?
[Persuadee] well, I'm glad to hear such a good news from this organisation. Education is must for everyone in the world. Therefore, we could help the children for their livelihood as well as for their education.
[Persuader] WHat do you think is the best way to help the kids? Education, food and water, something else?
[Persuadee] we can help them out their physical needs like good cloths, probably orphanage (home to stay) 
[Persuader] Yes, I agree too! I love that Save the Children goes to a lot of places to help with things like this. And did you know that only 5% of the money the charity raises goes administration (salaries for their employees and stuff)?
[Persuadee] yes I do, because it is need. Administration costs, like employees salaries, office bills and other expenses can be taken from the donations & it should be 5% as you said. 
[Persuader] Yes, I think they are great. Did you know that you can donate a little of the money you are earning today to them? It can help a lot of kids - from the hungry in the US, to the children literally being killed in war zones. It would help so much.
[Persuadee] I would love to help them a little bit (as per my ability), it will also helpful for those children to have a better life than the others.
[Persuader] That's amazing! I know finances are hard for everyone these days, so it is wonderful that you are willing to donate! How much would you like to give? May I suggest $.50 or even $1 if you are able?
[Persuadee] as per today's earning is very little I would like to donate 1
[Persuader] Thank you for your help! The amount will be deducted directly from your payment and sent to Save the Children.
```
</details>

### 7. `20180808-035715_390_live`  —  old modifier: `deferred`

**Why:** Persuadee hedges "I'll start with $1 and maybe give more later" but the Persuader then explicitly re-confirms just the $1 ("So $1 is your donation?") and the Persuadee answers cleanly: "Yes, $1 - thank you." The hedge about extra money is resolved out of the final position.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello, how are you doing today?
[Persuadee] Good thanks! You?
[Persuader] Very well. Do you have any particular hobbies that you enjoy?
[Persuadee] Mostly into hiking these days - how about you? Do you have any info on this children's charity we're supposed to talk about?
[Persuader] I like to play golf, as well as go on walks with my dog. Yes, the charity sounds like it does a lot of great work.
[Persuadee] Walks with the dog sound awesome.  I wasn't given any information about the charity but am happy to help.
[Persuader] Great! I have three children myself, and the welfare of children around the world is a very important cause to me. Save the Children is an international organization that is not involved with any government, and they're able to promote children's rights and support kids in developing countries.
[Persuadee] Sounds like great work.  I donate to a lot of different causes but am happy to pitch in. Are we attempting to agree on a donation amount?
[Persuader] That might be a good idea. Just to give some more info, they are a charity you can trust to actually do the work they promise to do. Any donation we give will make an impact around the world.
[Persuadee] Very cool, I have heard of them but never looked into them too closely. Do you already donate to them? Monthly or one-time?
[Persuader] You can do either. I prefer monthly, just so it fits in my budget easier. 
[Persuadee] Sounds good. Suggestions on a donation amount?
[Persuader] How about some of the payment from this HIT? Any amount from $0 to all of your payment would help.
[Persuadee] Sure, I'm happy to donate half the payment for the HIT
[Persuader] $1 will help a lot, but $2 would really help them reach kids around the world. I would rather get all of the payment too, but helping kids is better than spending that $1 on a candy bar or other snack instead.
[Persuadee] I'll start with $1 and maybe give more later :)
[Persuader] That's okay. Just so you're aware, a large part of their work is in war zones such as Syria. In the first two months of 2018, around 1,000 children were killed or injured due to violence there. Save the Children works to provide relief in countries like that.
[Persuadee] Yeah I've seen a lot of the news on Syria, it's horrible.  I work with Doctors Without Borders too, glad there are multiple players in the region to help!
[Persuader] So $1 is your donation? I'm sure that Save the Children will put it to good use!
[Persuadee] Yes, $1 - thank you
```
</details>

### 8. `20180826-013831_953_live`  —  old modifier: `deferred`

**Why:** Final line: "Okay. I'll donate half of that. So $1." - clear, resolved, no hedge anywhere in the dialogue.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi, can I interest you in making a donation to Save the Children?
[Persuadee] Sure
[Persuader] Would you like some information about the charity first?
[Persuadee] Yes, that would be helpful.
[Persuader] It's an international organization that provides relief and helps support children in developing countries.
[Persuadee] That sounds like a worthwhile cause.  
[Persuader] Yes, and your donation would be essential in helping ensure children's rights to health, education, and safety.
[Persuadee] That sounds great.  Are findings tax deductible?
[Persuader] Yes, donations to the charity are 100% tax deductible 
[Persuadee] Col.  Just out of curiosity, what developing countries does this charity focus on ?
[Persuader] They help children across 120 countries. Africa appears to be the continent where the charity focuses on as it serves 32 million there. 17.5 million Asian children are also served by the charity.
[Persuadee] Wow.  That is a huge impact.
[Persuader] Yes. The charity also helps children in the US who are growing up in poverty.
[Persuadee] Outstanding.  I see no reason not to help this charity.
[Persuader] Great! Your donation will be deducted from your payment in this task. You can decide how much you want to donate.
[Persuadee] Great.  What is my payment for this task?
[Persuader] $2 I think
[Persuadee] Okay.  I'll donate half of that.  So $1.
[Persuader] Awesome. The research team will collect the donation and send it to Save the Children.
[Persuadee] Super.  Thank you.
```
</details>

### 9. `20180826-033211_245_live`  —  old modifier: `deferred`

**Why:** After earlier hedges and deferrals ("I will defiantly be donating at the first of September"), the negotiation resolves to a final firm figure: "Sure I will donate 30%," confirmed by the Persuader as the closing deal ("I am going to Donate 70% and you will do the 30%. Good Deal").

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi how are you this day ? 
[Persuadee] Hey, I'm doing great, how are you?
[Persuader] I am very good. Glad to be doing this survey because it is for a good cause (Save the children) Do you agree ? 
[Persuadee] Oh absolutely! I think it's very important to donate to charities.
[Persuader] Yeah I stronlgly believe we should all pitch in and help. I am 100% sure I am going to donate 80%-100% of my earnings for this survey to (Save the children) It will make me feel good to help Little helpless children. What do you think you will be donating ?
[Persuadee] I don't have the money right now to donate. I will defiantly be donating at the first of September though. I will try to donate at least five dollars.
[Persuader] We all need money, but this is a special cause and the money is not too much. These surveys are a good way for us to get involved and help those in need........Dont you agree ?
[Persuadee] Oh yeah defiantly. Out of the earnings I earn from this survey I would probably donate at least half. It's only fair.
[Persuader] Wow that is so good to hear it reallly shows that most people are willing to help those who are less fortunate than ourselves. 
[Persuadee] Yeah it's very important to help someone that is less fortunate than yourself. Especially if they are children.
[Persuader] Did they tell you "How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment."
[Persuadee] At this time I can't donate any amount. However I will donate later.
[Persuader] I thought you said you would donate a part of your earnings ? How about I match you on what you decide you can afford to donate. If you donate 30% I will donate 50% if you donate higher I will increase mine accordingly. It is a one time thing. Those kids suffer quite a lot and dont really have anyone to help them. 
[Persuadee] Sure I will donate 30%.
[Persuader] Awesome. I know I have never met you ,but I feel so good to be working with you to help someone even if it is such a small amount it makes me feel glad. 
[Persuadee] Same to you! Most people wouldn't give anything and it makes me really happy to meet someone that would help with whatever they can.
[Persuader] Yeah I agree 100% with you. I have been to other countries that are very poor and it is Amazing how much a little donation will make a BIG differance in these childrens lives. 
[Persuadee] I guess in America you don't really understand what other countries go through. That's awesome you have been to other countries. I don't mind helping at all.
[Persuader] I live in Florida. What part of USA are you from ? 
[Persuadee] North Carolina, I've been to Florida once, it's nice.
[Persuader] North Carolina is nice I have been there once. Well nice talking to you so I am going to Donate 70% and you will do the 30% .Good Deal and hope this will help others. Take care have a great day.
```
</details>

### 10. `20180826-053845_531_live`  —  old modifier: `deferred`

**Why:** Final line: "I will donate all of my payment." No hedge or deferral anywhere in the dialogue.

<details><summary>Full dialogue text</summary>

```
[Persuader] Save the Children is an amazing charity that helps kids who are in desperate need. They can help with safety, education and more. You can donate some of your earnings to this amazing charity.
[Persuadee] I believe in this charity, but still wonder how much of the money I donate actually helps.
[Persuader] Every little bit makes a difference. When you have people who are so poor, it's amazing what a tiny amount can do.
[Persuadee] I would gladly give my earnings to this charity.  Children hold the future of the world.
[Persuader] It is really so heartbreaking when you see all of these kids not having enough to eat. It really breaks the heart. They are so little. 
[Persuadee] I know, it always amazes me how many children are suffering around the world.  It is so sad.
[Persuader] Even the little bit you donate from your earnings can go a long way to making a difference for a child. 
[Persuadee] Though MTurk they should raise quite a bit.  Even though it is only .30 for this hit, with the number of people it adds up.
[Persuader] That's what happens. Even small amounts make such a big difference when they are added up. That's why it does make such a difference to even do small things. 
[Persuadee] In my personal life I do pay attention to all the details and the reviews of charities.  There are so many worthy causes that I try hard to make sure my meeker amounts go to benefit the most. 
[Persuader] And Save the Children is a great charity. They really do help so many kids and people. 
[Persuadee] I know they are a well established charity so should have all the resources, administration wise, to get the money where it is needed most.
[Persuader] I think it's wonderful that you are doing this and are going to donate. It is such a great thing to do. 
[Persuadee] It makes me feel that even though not enough I have done a little something.
[Persuader] You do what you can, and that is all that matters. But you should feel good about this little amount. 
[Persuadee] I live in a very rural area, people in my town are extremely poor and it still amazes me how they will take what little they have and take care of each other.  
[Persuader] It is very sweet. And these small things just make such a difference. 
[Persuadee] It is hard to watch and not reach out to help a child.  I do what I can in my own community and the town comes together this time of year to make sure each child has school supplies.  It is really sad that Save a Child exists, the world should be a safe place for children and there should be no need. 
[Persuader] It should be. But with people helping it can at least make a difference. I think everyone can do their part. 
[Persuadee] I agree, it has been very nice chatting with you and I hope you have a great day.
[Persuader] Thank you so much. Can you tell me now how much you would like to donate? You can choose any amount to all your payment.
[Persuadee] I will donate all of my payment.
```
</details>

### 11. `20180826-054344_65_live`  —  old modifier: `deferred`

**Why:** Firm $500 commitment, explicitly reconfirmed: "Yes you can count on my donation." The later talk of asking coworkers to also give is a separate ask about other people, not a hedge on the Persuadee's own $500 pledge.

<details><summary>Full dialogue text</summary>

```
[Persuader] Would you be willing to donate your proceeds to the Save the Children organization?
[Persuadee] Certainly as long as I know the donation will help the children 
[Persuader] This is a fine organization.  I have done some research and the majority of the proceeds go directly into helping the children. 
[Persuadee] I would certainly be willing to donate then
[Persuader] How much are you willing to donate?
[Persuadee] I would be willing to donate $200
[Persuader] That is very generous.  Would you be willing to donate a bit more.  Say $500? From what I have learned, by donating $500, another organization will match the donation with a minimum $500 donation.
[Persuadee] I would certainly increase my donation if it would be matched since the majority of it is going directly to the children
[Persuader] That's wonderful!  So I can count on you for the $500 donation?
[Persuadee] Yes you can count on my donation
[Persuader] Thank you so much,  you have no idea how much this will help the children in need! 
[Persuadee] Thank you Glad I was able to help  this organization with my donation
[Persuader] Do you have any friends or coworkers you might be willing to donate as well?
[Persuadee] I could certainly ask some of my coworkers and tell them about the match if they donate at least $500 and tell them what a worthy cause it is.
[Persuader] Or how about an office pool to raise money?
[Persuadee] We really dont have a big office so I dont think an office pool would get very much in donations
[Persuader] Ok, that makes sense.  Anything you could get in donations would certainly help.  It doesn't have to be a full $500 donation. 
[Persuadee] Alright I will ask my co-workers
[Persuader] Thank you again for your willingness to help with this wonderful organization!
[Persuadee] Glad I was in a position where I was able to help
```
</details>

### 12. `20180826-061846_932_live`  —  old modifier: `deferred`

**Why:** Wants to give 100% of task payment and confirms the mechanism: "Awesome. I will do that." No hedge word anywhere.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi! How are you doing today?
[Persuadee] Good how are you? 
[Persuader] I'm pretty good. Have you ever heard of the Save the Children organization?
[Persuadee] I have heard of that organization. I have seen a lot of commercials on TV for it. 
[Persuader] I hear you. That is when I first heard of it as well. I love the fact that it is a non-government organization that promotes children's rights and helps to provide the support in those developing countries.
[Persuadee] Agreed. Any organization who promotes rights for those who don't have the platform to speak up is a wonderful charity. 
[Persuader] I guess now I am going to sound like the tv commercial but have you ever thought about donating to the organization? 
[Persuadee] I have thought about it in the past. 
[Persuader] I understand that. With all the organizations out there it is hard to tell a good one and a bad one. This organization helps to children with their rights to health, education, and even safety.
[Persuadee] Yes it is hard to tell whose interests really lie in the movement they promote. I like to research organizations first to see if the money I give is really going to the cause, or if it is wasted by high overhead costs. 
[Persuader] Yeah I totally understand that. I know the commercials are heart wrenching...seeing all those children suffer and hurting. It breaks my heart. 
[Persuadee] Absolutely. It makes you look at your own children (if you have any) and think if that was them how would I cope? It's the reason I go to work everyday. To make sure that they have all that they need, and more than I ever had. 
[Persuader] I completely understand that. I have a little girl and it only makes me want to do more and more for her. Did you know that you can donate a little to the charity today?
[Persuadee] I did not. 
[Persuader] Oh gosh you totally can. Whatever you are making for your task payment you can choose to send so much of that to the Save the Children organization. You can choose whatever amount that you want.
[Persuadee] How do I do that? I would like to give 100% of the task payment. 
[Persuader] After we are done talking they should ask you if you would like to donate some and you can enter in whatever amount you want. The research team gathers all the donations and send it all to Save the Children.
[Persuadee] Awesome. I will do that.
[Persuader] Oh gosh, that is so great of you. Even just a little helps them so very much. You are doing a wonderful thing but you and someone else. Now when you see those commercials you can feel good that you did something to help.
[Persuadee] Yes, it will be nice to know that I was able to give to them. 
[Persuader] Well I hope you have a wonderful day and on behalf of the charity and the children it is going to, thanks for your help.
```
</details>

### 13. `20180826-063853_537_live`  —  old modifier: `deferred`

**Why:** "I will gladly [donate]" is a clear, enthusiastic, unconditional acceptance with no hedge word, in direct response to "would you donate your earns from this task??"

<details><summary>Full dialogue text</summary>

```
[Persuader] hi..I;m mike
[Persuadee] Hello Mike I am Pete
[Persuader] hi..pete, hows your life
[Persuadee] My life is awesome and your?
[Persuader] it's great,I can't complain
[Persuadee] What do you do for a living?
[Persuader] I day trade stocks and try to help children organizations like save the children...have you ever heard of that organization before?
[Persuadee] I have heard about it but I do not know wgat they do
[Persuader] they help children that is in need of support and a healthy life change.
[Persuadee] Thats an awesome labor
[Persuader] I would like to ask if you would like to help by donating what you make from this task to the organization which will be a great help...what you think?
[Persuadee] I think children need help.
[Persuader] so would you donate your earns from this task??
[Persuadee] I will gladly .Are donating as well?
[Persuader] I would love too...thank you for your support 
[Persuadee] You are welcome.Children are the futere
[Persuader] yes they are..where are you from??
[Persuadee] I am from USA.What about you?
[Persuader] I'm from use too,new york
[Persuadee] Wow .Does Save the children has the offices there?
```
</details>

### 14. `20180826-070022_438_live`  —  old modifier: `deferred`

**Why:** Final line: "I'll donate $0.05" - a direct, unhedged answer to "how much are you willing to donate today?"

<details><summary>Full dialogue text</summary>

```
[Persuader] HI.Do you know about Save the Childre organization?
[Persuadee] I've heard of them but other then that no not much how about you?
[Persuader] I have.They help children in need
[Persuadee] Well, that's a noble cause don't you think
[Persuader] Of course.I have seen kids dying of hunger in those countries at war.It breaks my heart
[Persuadee] I can imagine, that is horrible..... to not be able to eat, or drink, and worry about being sick all the time
[Persuader] They are children.They did not ask fot this.
[Persuadee] well, I can't imagine anyone would much less a child....
[Persuader] How much money do you spend on candy?
[Persuadee] not much maybe a couple dollars every few months
[Persuader] Well that can make a difference in a children life
[Persuadee] I donate sometimes well, to other charities
[Persuader] This one ensure that children get the money
[Persuadee] That's always good, it's not good to donate somewhere that they don't give to what they're supposed to be donating to
[Persuader] Of course not.Many children in war zones are struggling 
[Persuadee] Horrible, I know..... war is like adults acting like children but worse because they know they're not showing regard to the people suffering
[Persuader] Are you commit to the cause?
[Persuadee] Of course I'll donate something
[Persuader] how much are you willing to donate today?
[Persuadee] I'll donate $0.05
```
</details>

### 15. `20180826-094859_742_live`  —  old modifier: `deferred`

**Why:** Final line "I will donate 25" is unhedged, but note this whole dialogue is a general chat about typical monthly charitable habits and never explicitly frames the $25 as being deducted from this task's payment - worth double-checking whether it qualifies as an in-task commitment at all.

<details><summary>Full dialogue text</summary>

```
[Persuader] hello
[Persuadee] hello
[Persuader] would you donate
[Persuadee] to what charity?
[Persuader] im saying for children
[Persuadee] ok, yes I probably would. About 25 a month
[Persuader] me too even its 5 dollar
[Persuadee] Do you think it's about children needing food or about disabilities in children?
[Persuader] to be honest i dont really know
[Persuadee] Ever see the Shriners Hospital commercials?
[Persuader] i use to yes
[Persuadee] Where you get the commemorative bear blanket if you donate a certain amount
[Persuader] that i dont know do you know
[Persuadee] Yes, they ask for 50 dollars a month, would you ever give that much?
[Persuader] i would because i know they need it
[Persuadee] Yes they do, many children with many different types of disabilities.
[Persuader] that right to
[Persuadee] So, we're in agreement, we would both contribute to this charity?
[Persuader] i would do 5
[Persuadee] I will donate 25
```
</details>

### 16. `20180826-180554_582_live`  —  old modifier: `deferred`

**Why:** Firm, unhedged commitment repeated twice verbatim: "I'll donate 5 dollars" and "I will donate 5 dollars," plus a final "yes I have in going to donate." No hedge anywhere.

<details><summary>Full dialogue text</summary>

```
[Persuader] Good evening how are you doing today?
[Persuadee] yoy AnAOk OIm I
[Persuader] I am writing to ask you to donate 10 dollars to save the children. This organization helps children's rights and supports children living in developing countries
[Persuadee] Yes I would
[Persuader] Your donation is essential to help ensuring children's rights to health, education, safety, etc. It will make a real difference in the world.
[Persuadee] I know it does I'll donate 5 dollars
[Persuader] We have many children who starve and die of hunger. You donation will stop this from happening and possible save a child's life
[Persuadee] I realize that
[Persuader] Save the children have been fight child hunger and disease for many years We have made a big inpact in these children's lives over the many years.
[Persuadee] That's is good
[Persuader] We have not received much support for these children. For instance, millions of Syrian children have grown up facing the daily threat of violence. In the first two months of 2018 alone, 1,000 children were reportedly killed or injured in intensifying violence. Your donation could possible go to this problem and help many young children
[Persuadee] Yes I know I will donate 5 dollars
[Persuader] This will help out tremendously!
[Persuadee] i know it will
[Persuader] If you could please ask you friends and family to help?
[Persuadee] I will are you going to help
[Persuader] Convince them that they waste too much money on unnecessary stuff like snack and candy. They could be helping people with their money'
[Persuadee] yes I know
[Persuader] Please look at our website  URL You can find out a lot about Save the children. It shows you all our sucess stories. 
[Persuadee] yes I have in going to donate
[Persuader] Okay great! Thank you so much for your time and donation. We appreciate any help we can get. Remember to pass along our info to friends and family. Thank You and good night!
```
</details>

### 17. `20180826-180631_700_live`  —  old modifier: `deferred`

**Why:** Final line: "I will donate half of my earnings." Clear, specific, unhedged.

<details><summary>Full dialogue text</summary>

```
[Persuader] hi! how are you today?
[Persuadee] Hello! I am good.  How are you today?
[Persuader] I am doing well thank you. Have you heard of save the children?
[Persuadee] I haven't.  What is it all about? 
[Persuader] It is an organization that helps raise money to help the children around the world
[Persuadee] I have a passion for children.  That would be a charity I would donate too for sure.
[Persuader] It is great. the children are our future and need the chance to have a full life
[Persuadee] I do agree 100%  How would I go about finding this charity?
[Persuader] they have a website at  URL  
[Persuadee] Thank you very much. I will look into it for sure and make a donation.
[Persuader] You can also donate after we finish here, too!
[Persuadee] That is awesome. I will definitely be making the donation.  
[Persuader] that's great! Do you ever volunteer?
[Persuadee] I do volunteer some.  I also take in children that would other wise go without. 
[Persuader] that is amazing! you are an excellent human being
[Persuadee] Thank you.  Do  you volunteer any where?
[Persuader] I work with chidlren of abuse. it's hard work, but they need help
[Persuadee] You are a wonderful person.  Those children need your help.
[Persuader] Well it was lovely chatting! how much will you donate today?
[Persuadee] I will donate half of my earnings.  It was lovely chatting with you.  Will you be donating?
```
</details>

### 18. `20180826-184037_209_live`  —  old modifier: `deferred`

**Why:** Mutually agreed, unhedged: "So I think that we should donate .10 each" / "Yes I am fine with that" / "We will donate .10." Note: like #40, this dialogue never explicitly frames the $0.10 as coming from the task payment - worth double-checking the in-task-commitment requirement.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello, how are you?
[Persuadee] Fine, thank you. How do you feel about donating to a children's charity?
[Persuader] I always they to donate when ever I am able. Especially childrens charities, children are so innocent and deserve the best chance at life.
[Persuadee] But do you really trust the charities that you give to? Do you know if they are actually using that money for the intended purpose?
[Persuader] YEs I always look into the charities that i donate to. For instance I always donate to our local childrens hospital because my nephew was treat there when he was diagnosed with cancer. I saw how many sick little kids where there fight for their lives. So I also donate to the hospital and childrens cancer network because the money goes directly to research cancers that effect children.
[Persuadee] I agree, the local charities are good. I don't trust the bigger charities. I think most of the money that is donated goes towards salaries, etc.
[Persuader] Sadly that is true some times. How do you feel about donating to childrens charities?
[Persuadee] I think it is better to help children yourself. That way, you know what the money is being used for. Also, when you do it yourself, it is a lot more rewarding.
[Persuader] True, but there are so many innocent little children who don't have access to food or clean water, not to mention basic health needs. We are lucky to have help if needed they have no one to turn to.
[Persuadee] How much do you usually donate every year>
[Persuader] I try to donate at least 250 every year. 
[Persuadee] That is good. Do you have any kids?
[Persuader] Yes, I have two and I have a lot of nephews and nieces, 1 has a lot of  health issues so childrens charities are always important to me. Do you have children?
[Persuadee] I do not have any children yet, do you think that having kids had a big effect on whether on not you are willing to donate to a children's charity?
[Persuader] Yes, probably but my nephew got sick before I had kids and thats what made me realize that cancer or any illness can happen to anyone whether its your child or some one close to you. It is the scariest thing that can happen to anyone especially a child. Once I saw how many children were fighting cancer and other serious disease it woke me up to what is important in life and just because we are not going through it there are so many children suffering that the least I can do is donate.
[Persuadee] That is a great way to think about it. I'm sure that when I have kids, my thinking will change a lot as well. So I think that we should donate .10 each to the children. What do you think?
[Persuader] Yes I am fine with that
[Persuadee] It is a small amount, but I think that every penny can make a lot of difference. If half the people in the world just donated 10 cents to such charities, then we would raise a LOT of money. It is not necessary to donate hundreds of dollars.
[Persuader] Yes that is what I believe to, We wouldn't even notice 10 cents we spend so much on coffee little things the .10 cents is nothing.
[Persuadee] Agreed. We spend so much money on other things, but the moment someone asks for a little charity, we make up many excuses. We will donate .10 and hopefully that will make a difference.
```
</details>

### 19. `20180828-192202_602_live`  —  old modifier: `deferred`

**Why:** Final line: "I will donate .50, and I will definitely visit your website to learn more about sponsoring a child." The $0.50 is unhedged and firm; the separate clause about visiting the website for more info is an additional action, not a hedge on the donation amount, and is itself stated with "definitely," not a hedge word.

<details><summary>Full dialogue text</summary>

```
[Persuader] Ho how are you?
 [Persuadee] I'm doing well. How are you?
 [Persuader] I'm doing great. My name is Kim and I work for a charity organization.
 [Persuadee] What type of charity organization do you work for?
 [Persuader] Our charity organization is called Save the Children. We are committed to providing health and nutrition programs that save children's lives and ensure they grow up healthy.
 [Persuadee] That's great. Does your work benefit children globally?
 [Persuader] Yes we have a global presence. We help Syrian children refugees and children in developing countries, especially in war zones. Save the Children is the voice for vulnerable children. We're on the ground in 120 countries, working to reach every last child through international programs that focus on health, education, protection and disaster relief. Together, we're changing children's lives and the future we all share.
 [Persuadee] Well, that definitely sounds like a worthwhile cause. Can I ask what percentage of donations received go to helping children versus the percentage that goes to the administration of the charity?
 [Persuader] Save the Children has a proven track record of using donations efficiently and effectively. Our independently audited financial statements consistently show that nearly 9 out of every 10 dollars we spend goes to programs and services for children and families in need. We keep administrative costs low so that more funding goes to children's programs. In fiscal year 2017, 86% of all expenditures went to program services, 9% went to fundraising and 5% went to management and general. 
 [Persuadee] That's incredibly impressive, much better than other charities I've looked into. It must be very rewarding to be able to impact the lives of so many people.
 [Persuader] Yes, In the first two months of 2018 alone, 1,000 children were reportedly killed or injured in intensifying violence. Every donation will indeed be a help a lot of children and their families. We target the major causes of maternal, newborn and child deaths and provide the best health and nutrition programs to save children's lives and ensure they grow up healthy.
 [Persuadee] Does the charity offer the ability to sponsor an individual child and be kept up to date on their progress?
 [Persuader] Yes you can! Through child sponsorship, you can be the hero in the life of a child in need. You can make sure they grow up healthy, educated and safe. Through the power of Sponsorship, you help ensure a child in need has the best chance for success _ with a healthy start, the opportunity to learn and protection from harm. Our innovative Sponsorship programs address the unique needs of children where they live
 [Persuadee] That's something I would definitely like to learn more about. I'll visit the charities website and check it out. 
 [Persuader] Yes thank you. There are many ways to help. For more information, and if you are willing to help or make a donation, you can go to our website: URL Will you be interested in making a donation to Save the Children ?
 [Persuadee] Yes, I would love to help this charity! It's a great cause.
 [Persuader] How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2).
 [Persuadee] I will donate .50, and I will definitely visit your website to learn more about sponsoring a child.
 [Persuader] Thank you so much for your donation. The research team will collect all donations and send it to Save the Children. There are many more ways to donate to Save the Children and you can learn more by visiting our website.
 [Persuadee] I definitely will! Thanks for informing me about this great opportunity to help.
```
</details>

### 20. `20180830-154630_337_live`  —  old modifier: `deferred`

**Why:** Final line "Yep!" directly confirms "you felt like donating 30 cents was fair?" - a clean, unhedged final confirmation.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello
[Persuadee] Hi
[Persuader] So I am supposed to persuade you to donate all thirty of your cents to a charity called Save the Children
[Persuadee] Oh, I believe I've heard of them. What kind of work do they do?
[Persuader] They promote childrens rights, provide relief and helps support children in developing countries
[Persuadee] Do you know if they keep track of the effectiveness of their interventions?
[Persuader] I believe they do. They also help fund education for children
[Persuadee] That sounds admirable. I usually donate to global health charities (like the Against Malaria Foundation) because it's highly cost effective. Policy intervention is also important, but it's harder to know if it's worthwhile/will be successful...
[Persuader] Totally understandable. It is easier to donate to something when there is tangible evidence of its success. I think helping children have access to an education will be beneficial to the entire world in the long run
[Persuadee] By the way, on my side I'm told I can donate anything from $0-$2. So donating $0.30 sounds reasonable.
[Persuader] I think that is very reasonable, and every little bit helps. 
[Persuadee] I would be interested to know what different programs their funding goes towards. Do they publish a budget?
[Persuader] They actually do, I just looked on their website. It has a lot of information that I didnt expect them to make public
[Persuadee] That's great! It's encouraging when a charity is transparent. I assume it's a 501.3(c)?
[Persuader] It looks like it, only 5% of their donations go to management so I believe they operate as a non profit. Which is wonderful
[Persuadee] Do you have a favorite non-profit? :P
[Persuader] I should probably say this one but I donate to animal shelters mainly haha
[Persuadee] Oh nice. I'd also like to look into donating more to animal welfare charities. I know there's some philosophical disagreement about this, but I prefer to diversify my charitable 'investments' as it were.
[Persuader] That makes sense! So, you felt like donating 30 cents was fair?
[Persuadee] Yep! Good talking with you.
```
</details>

### 21. `20180830-155510_301_live`  —  old modifier: `deferred`

**Why:** "I would be willing to donate 0.75 of mine no question." The phrase "no question" explicitly removes any hedge from "would be willing."

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi! How are you doing today?
[Persuadee] Hi there, I am doing ok how are you?
[Persuader] I'm not doing too bad. Thank you!
[Persuadee] How has you day gone today?
[Persuader] Not too bad, I just got in from work a few minutes ago. I'm glad it's almost the weekend.
[Persuadee] Yes, I always look forward to the weekend.  Now college football is fixing to start up and I am even happier!
[Persuader] Yes it is. College football and a 3 day weekend. It can't get much better than that. Who's your team?
[Persuadee] I am born and bred TCU football so they are and will always be my team, what about you?
[Persuader] I'm an Auburn fan myself.
[Persuadee] How do you think they are going to do this year?  I know Alabama is going to be tough as usual
[Persuader] I think they'll do ok. I expect them to stay at least in the top 15. They're a young team this year, but it seems like they always are. Our QB has had some shoulder issues this offseason so we'll see how that plays out. Our run game should be strong though. Alabama is going to be tough as long as Saban has a hand in that organization.
[Persuadee] Isnt Stidham your QB still or is he graduated, I know he was from Baylor and really good!
[Persuader] Yeah he's still there. He did really well last year.
[Persuadee] Nice, well we play Ohio State and I think 99% of the country is going to be rooting for us to win because of Urban Meyer lol.
[Persuader] Yeah, hopefully you guys will. Urban's going to be the nasty face of CFB this year.
[Persuadee] I just cant believe the flimsy excuses by the university to be honest, all they really care about is winning.
[Persuader] Yeah that's the way it is these days. It's sad.
[Persuadee] besides auburn obviously, who would you pick in the final 4 playoffs?
[Persuader] I think it'll be Alabama of course, I'd like to see TCU, you guys always seem to be a contender, I'd like to see Michigan, and anyone but Clemson lol.
[Persuadee] Haha, my sleeper team is West Virginia I think they have a chance to be really good, their QB might be the best pro prospect this season.  I think we will finish in the top3 of the B-12.
[Persuader] I'd like to see someone else besides an SEC team win it honestly. This coming from an unbiased SEC fan.
[Persuadee] That is nice, I agree with you about Clemson though, it should be fun though regardless!
[Persuader] Yeah it should be. It's been nice talking to you. I guess I should get to the point of the chat. Would you like to donate any of your earnings to Save The Children?
[Persuadee] Sure they are a reputable charity and I have seen their work on TV.  I would be willing to donate 0.75 of mine no question.
[Persuader] Thank you for you donation. Good luck to your team this year! Go Frogs!
[Persuadee] Good luck to you too, Go Tigers!
```
</details>

### 22. `20180830-190109_662_live`  —  old modifier: `deferred`

**Why:** Final line: "you can put me down for .50 :)" - unhedged, specific, resolved.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello there, how are you doing today?
[Persuadee] Good. How about you?
[Persuader] Great! I'm doing well, thanks for asking. Have you ever heard of a charity called Save the Children?
[Persuadee] Yes I have. I remember it from the 90s.
[Persuader] Right on. So you understand how imperative it is that they stick around, as they help support and provide relief for children in developing countries.
[Persuadee] Yes glad they're stil laround
[Persuader] So, the researchers of this study are actually doing something very cool. You can help this charity directly by donating some or all of your earnings to Save the Children.
[Persuadee] Oh ok that sounds good
[Persuader] Yeah, it's super cool! Even a small donation of 50 cents is great when lots of other people are donating too. Would you be interested in donating some of your task earnings?
[Persuadee] yes i would
[Persuader] Awesome. How much of the $2 would you like to donate?
[Persuadee] you can put me down for .50 :)
[Persuader] Thank you so much! It always feels good to help out others, I think.
[Persuadee] Yes it does
[Persuader] If you'd like to  find out more info about this charity, you can go to their website at  URL  Do you have any questions? :)
[Persuadee] No I don't :)
[Persuader] For sure. Well it was a pleasure "meeting" you today!
[Persuadee] Have a good one!
[Persuader] You too my friend.
[Persuadee] How do we end this?
```
</details>

### 23. `20180830-194021_927_live`  —  old modifier: `deferred`

**Why:** "Okay. Well I can give 10% of my payment, so 20 cents." No hedge; the Persuadee explains why they won't go higher but never retracts the 20-cent pledge.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi
[Persuadee] Hi. How are you doing tonight?
[Persuader] Great!  How are you?
[Persuadee] Doing very well, thank you.
[Persuader] I want to ask you a question?
[Persuadee] Okay, what is the question?
[Persuader] Would you be willing to donate some of your payment for this task to a children's charity called Save the Children?
[Persuadee] How do I know that the money will actually go to Save the Children?
[Persuader] The research team will collect all donation and send it to Save the Children.
[Persuadee] How reputable is the organization?
[Persuader] Very reputable. Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries.
[Persuadee] Okay. Well they sound like a good organization. I already donate monthly to another organization that has similar goals.
[Persuader] That is great to hear! But Save the Children does need your help. Your donation will help, among others, children and their families that are suffering from hunger.
[Persuadee] Okay. Well I can give 10% of my payment, so 20 cents. 
[Persuader] That is very generous. But let me ask you: is there any way you can go even a little higher.  It would mean a lot. Many of the children Save the Children helps are from war torn areas of developing countries. In these areas, in the first two months of 2018, 1,000 children were killed or injured. Your donation will help Save the Children assist children in those areas.
[Persuadee] I understand that. Like I said I already to donate to something similar, but at this point in my families life we really need as much money as I can bring in.
[Persuader] Understood.  Thank you so much!  I know your donation will help.
[Persuadee] I hope it does. Thanks for being understanding.
[Persuader] Thank you as well.
[Persuadee] Have a good night.
```
</details>

### 24. `20180831-052816_178_live`  —  old modifier: `deferred`

**Why:** States "I am willing to donate 10 cents" three times, including once defensively reasserting it against pushback ("I am not 'only' willing. I am willing to donate 10 cents.") No hedge anywhere.

<details><summary>Full dialogue text</summary>

```
[Persuader] How would you like to donate to save the children
 [Persuadee] whats that?
 [Persuader] It's an excellent charity that helps get children the necessary things that they need to survive
 [Persuadee] sometimes i donate to charity, but when someone comes right out and asks it feels a little pushy ya know?
 [Persuader] I understand that, but sometimes you just need to be made aware of some excellent charities
 [Persuadee] Yes i am aware of many problems in the world.
 [Persuader] Right and I understand how most people don't think that they need to help children in other countries, but if we don't then who will. These children need all the help that they can get.
 [Persuadee] I agree with that.
 [Persuader] I'm willing to donate 1 dollar to this cause are you?
 [Persuadee] i can only make a small donation of 10 cents. will you accept that?
 [Persuader] I'm willing to accept any amount that you are willing to donate, but wouldn't you like to be able to donate a little more to help the poor defenseless children?
 [Persuadee] I would love to solve all the problems of the world, but i can only do what i can do today. i can donate 10 cents.
 [Persuader] Ok I'm happy to at least get something. So out of your two dollar payment you are only willing to donate 10 cents?
 [Persuadee] I am not "only" willing. I am willing to donate 10 cents.
 [Persuader] Alright thanks for being willing to donate.
 [Persuadee] You are welcome, in the future i would work on some interpersonal skills. that will assist you. i promise.have a good day.
 [Persuader] In the future I would work on my willingness to donate more
 [Persuadee] what makes you think im not homeless myself?
 [Persuader] I don't want to argue with you
 [Persuadee] its a simple question, and again you could learn alot from interpersonal skills. have a good day. good bye.
```
</details>

### 25. `20180831-073753_874_live`  —  old modifier: `deferred`

**Why:** Final line: "I am willing to donate the entire amount I would have recieved from the task." Unhedged, 100% of task payment.

<details><summary>Full dialogue text</summary>

```
[Persuader] Good morning! I am in hopes you will share your earning as I have to a charity close to me heart called Save the Children.
 [Persuadee] Goodmorning! I would love to hear more about Save The Children
 [Persuader] Many details are here on this web site. URL 
 [Persuadee] Thank you, I will look. Can you tell me how much the donations goes toward the charity?
 [Persuader] Save the Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries.
 [Persuadee] It sounds like a great charity! I am reading a bit about it now.
 [Persuader] It is a great thing for children! Each donation is essential to help ensuring children's rights to health, education and safety. I plan to donate my payment for this task as every little bit helps.
 [Persuadee] I think it's important that children's rights are protected. So many times they are forgotten. I would also be willing to donate as well. 
 [Persuader] Each donation will go to a trust-able fund for the children which makes me trust and know my donation is going to the right place and for the right reason.
 [Persuadee] that's great. I'm weary of certain charities but this one sounds legitimate 
 [Persuader] I too am weary of such charities but this one has all the information and facts are checked to ensure it is the real deal.
 [Persuadee] Great. I want donations to actually get to those who need them
 [Persuader] Exactly my thoughts!! Small donations will indeed help a lot of children and their families
 [Persuadee] and looking at the website- even the small donations help a great deal
 [Persuader] Yes they do!! I think about how I have not given much thought to when I buy a bag of candy or a snack but the small amount I spend could mean big help for them.
 [Persuadee] Exactly, the money I spend on coffee or other non-essentials could be put to much better use
 [Persuader] I am glad you too see the benefit of small change to make a huge change for the children!! I am going to donate my payment from this task, how much do you think you would be willing to donate from this task?
 [Persuadee] I am willing to donate the entire amount I would have recieved from the task
 [Persuader] That is truly awesome!! Together we are going to help make small change into something bigger!!
 [Persuadee] It's a good way to start the day :)
```
</details>

### 26. `20180831-094601_58_live`  —  old modifier: `deferred`

**Why:** Final line: "I will donate 20 cents." No hedge anywhere in the dialogue.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello
 [Persuadee] Hi! How are you?
 [Persuader] doing good... what about you
 [Persuadee] I'm pretty good. Thank you for asking
 [Persuader] What we are going to discuss here?
 [Persuadee] I am not sure, about charity maybe?
 [Persuader] okay.... i think this is about children's charity
 [Persuadee] Tell me more about it
 [Persuader] This is a charity program to collect money for the upliftment of the kids 
 [Persuadee] What is the name of the charity and what are the programs?
 [Persuader] this is the charity to save the children.... would you like to donate something
 [Persuadee] Is it trustworthy and how does my charity benefit the children?
 [Persuader] All the amount donated by you is going for the charity
 [Persuadee] What are the programs? 
 [Persuader] It will promotes children's rights, provides relief and helps support children in developing countries.
 [Persuadee] Where is the headquarter of the charity?
 [Persuader] Headquarter is in fairfield, CT. you can visit URL 
 [Persuadee] Are there any program for kids in US?
 [Persuader] Yes there are some. Would you like to donate. you can do it after this conversation
 [Persuadee] I will donate 20 cents
```
</details>

### 27. `20180831-222729_66_live`  —  old modifier: `deferred`

**Why:** After an initial "Maybe. I am not sure yet," the dialogue resolves cleanly: "Nice So we will each donate 50 cents, right?" / "Yes 50 cents." The last clear position is unhedged.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello, Have you ever donated to a charity?
 [Persuadee] A few times, yes. 
 [Persuader] ow was your experience?
 [Persuadee] It was ok. I didn't really think much of it. Most of the time its just a dollar or two.
 [Persuader] Do you donate all te time?h
 [Persuadee] Not so much.
 [Persuader] Have yu heard of \\Save the children? It is pretty well known around the world.
 [Persuadee] I think so.
 [Persuader] What do you think that they do?
 [Persuadee] Give money to child. Support efforts in war torn countries. Healthcare. All that stuff.
 [Persuader] eah, pretty much and it gives you the good feels kowing that you have helped to change a childs life
 [Persuadee] You could say that.
 [Persuader] I plan to make a sizeable donation today as a mattter of fact and wondering if you would like to join me so that the doatiowould go eve further than if just one person doates?nn nn
 [Persuadee] Maybe. I am not sure yet.
 [Persuader] What concerns do you have about the charity?
 [Persuadee] Where the money goes. Lots of charities have massive ''administration'' cost.
 [Persuader] Well, i don't have all of the exact details but i can honestly tell you that it will be sent directly to the charity so that they can dispurse it accordingly.
 [Persuadee] Hm. I see.
 [Persuader] Plus, just like all other charities it takes a lot of faith to send money and Save the Children is the type that relys on faith since they have been around for many years. This experience is what makes me continue to donate to them. So would you like to donate? If you would, how much would you like to donate with me?
 [Persuadee] Well, that depends what you are going to donate.
 [Persuader] I plan to donate 50 cents
 [Persuadee] Sounds like a plan.
 [Persuader] Nice So we will each donate 50 cents, right?
 [Persuadee] Yes 50 cents
 [Persuader] Great!@ Thanks so much and God bless you!
```
</details>

### 28. `20180901-100753_363_live`  —  old modifier: `deferred`

**Why:** Earlier hedge ("would have to discuss this matter with my wife first") is superseded once the wife turns out to be unavailable; final line reaffirms plainly: "I will give 50 cents today and look into a fundraiser with my church group." The 50-cent pledge itself carries no hedge.

<details><summary>Full dialogue text</summary>

```
[Persuader] How are you doing today? Are you familiar with the charity Save the Children?
[Persuadee] Good, you?  Never hard of it.  Is it a charity?
[Persuader] I'm great, thanks for asking. Yes, it is a charity. I'm working with them to secure donations to help children in need. Helping families with children through crisis periods in their lives like relief after hurricanes, flooding, and earthquakes. We are also accepting donations to aid refugees and to assist with housing needs. Does this sound like a charity you would be interested in supporting?
[Persuadee] Yes I am interested.  Do you have a website?
[Persuader] Yes! Please visit  URL for additional information. But I might be able to answer any questions you have at this time.
[Persuadee] I am going to look at it really quick.  How much do people usually donate?
[Persuader] The donations vary. Today, I'm asking for a donation of $5. Of course, anything above that would be greatly appreciated. 
[Persuadee] Pretty sure I can only donate up to $2
[Persuader] A $2 donation from the heart is better than no donation at all! Your support is greatly appreciated. Did you look over the website?
[Persuadee] Honestly everthing I make here goes into my son's college fund.  I was more thinking 50 cents. I did look at the website. looks like a really good cause.
[Persuader] I understand your need to budget for your own children. Please keep in mind that your donation will be directly deducted from your task payment. Wouldn't you consider it worth the effort to donate the entire $2 for charity. Your $2 can make all the difference in the lives of these children. $2 could be several meals for a child in need. 
[Persuadee] I would have to discuss this matter with my wife first.  I am only comfortable with giving 50 cents right now.
[Persuader] Thank you for your continued support and donation. Would you be able to discuss the donation with your wife at this time? I ask because time is essencial. Millions of children are facing the threat of starvation, illness, and homelessness while we speak. 
[Persuadee] She's not home right now.  But I would be willing to bring this up with my church group and maybe do a fundraiser for this cause.
[Persuader] That would be incredible! Additional support from your church group is much appreciated as well. Again, thank you for your support and commitment to Save the Children. Charitable causes, especially those concerning children and the less fortunate, are definitely the Lord's work! And I know what goes around comes around. And God rewards those that look out for the less fortunate.
[Persuadee] Do you know if my donation can specifically go to their US program that help border children?
[Persuader] I believe the funds can be specifically allocated to that designation. I'm happy to hear that you have a passion to help the needs of those children. But there are millions of other children throughout the world that need our assistance. Would you be able to donate $2 directly to those children? I know that especially now, they need all the help they can get. I'm not sure when your children will be going to college, but these kids are in need of help today!
[Persuadee] I appreate the info.  I will give 50 cents today and look into a fundraiser with my church group.
[Persuader] I understand. We will accept your 50 cent donation today. Please use the link I provided earlier for additional information to give to you congregation. There is also info on that site as to where to send future donations. 
[Persuadee] Thanks.  Have a good day!
[Persuader] Again, thank you for being part of the solution. It is greatly appreciated. Have a great rest of your day!
```
</details>

### 29. `20180901-180119_88_live`  —  old modifier: `deferred`

**Why:** Task-specific amount is firm and was raised on request to $1.75 ("Hmm ya I can help .25 cents more"). The closing remark about donating "on the regular" concerns future/ongoing giving in general, not a hedge on the $1.75 already committed.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi.  HOw are you
[Persuadee] Pretty good, whats going on today?
[Persuader] not much.  do you donate to any charities
[Persuadee] I do, I love helping out people in need or need something to help them get going.
[Persuader] How about donating to Save the children?
[Persuadee] It sounds like a great cause, can you tell me about it?
[Persuader] Yes, the money helps children with clothing, food and school
[Persuadee] That all sounds wonderful, I would love to donate to that.
[Persuader] Howmuch do you think you can donate
[Persuadee] I want to donate 1.50 to help the children get better lives.
[Persuader] That's great.  So wonderful for you to do that.
[Persuadee] Yeah, the kids will really benefit from everyones help.
[Persuader] Would you like to maybe donate 1.75 instead of 1.50?
[Persuadee] Hmm ya I can help .25 cents more.
[Persuader] Have you donated to this cause before?
[Persuadee] No I havent, this is my first time hearing about it.
[Persuader] So glad you decided to donate.  This will really help
[Persuadee] You are very welcome, thank you for introducing me to this great charity.
[Persuader] Do you think you will continue to donate to this charity
[Persuadee] Yeah I will donate on the regular.
```
</details>

### 30. `20180901-183912_261_live`  —  old modifier: `deferred`

**Why:** "I would be willing to give $1.00" - decisive, specific; "and then I'll investigate it more" is a separate future research action, not a hedge on the $1.

<details><summary>Full dialogue text</summary>

```
[Persuader] happy friday! have you caught any of the college football games today?
[Persuadee] No I have not.  I'm not a big fan of college football.
[Persuader] I'm a big gator fan. But that's about it. How have you spent your weekend? i just realized today is Saturday and not Friday. I had to work this morning so it threw me off.
[Persuadee] **laughing**  It's hard for me to keep up with what day it is too.  I've been out of work for a few months now, so every day seems like a weekend.  I'm planning a family get-together for tomorrow so I'm excited about that.  What plans do you have?
[Persuader] that will be fun! what industry are you in when you're working?
[Persuadee] I've worked in the engineering department for alot of years.  Some has been project management, some drafting, and some assisting.  
[Persuader] my husband is an engineer. Great industry. You'll find a new job in no time. 
[Persuadee] Yeah.  The problem is last year both of my parents died at almost the same time (withing 1 1/2 hours of each other).  I had been taking care of them for about 7 years.  Between that and dealing with my sister and the will, it took a major toll on me.
[Persuader] i am so sorry to hear that!!!!!!!!!!!!! i can't even imagine what life must be like. you have two angels on your side now. they will take care of you from a better place.
[Persuadee] You are so right!!  I miss them terribly, but am so glad that they are not suffering anymore.  I bought their house out from my sister, but it's been a struggle as far as the job I had.  They were great and tried to keep me on as long as they could, but we found mold in the house and I've been really sick. 
[Persuader] i hope you get well soon. there has to be some positivity coming your way soon after all this rough stuff.
[Persuadee] I know there is!  Sometimes there are tough things in life, but if you stay strong in your belief you will make it through.  One of my daughters and I have been working to get the house in order.  I really enjoy working with my daughters.  Do you have kids?
[Persuader] i do! I have a daughter and a son. We are doing a 5k tomorrow. it's good to spend time with the kids.
[Persuadee] oh wow!!  Impressive!!  I can't imagine doing that, but I was never very athletic!!  lol   I could see one of my granddaughters doing that though.
[Persuader] it's good to get out every once in a while. are you familiar with save the children the charity?
[Persuadee] I'm not familiar with that charity.  What is it about?
[Persuader] It is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries. Every little bit helps. Would you be willing to make a minimal donation? less than a dollar would help.
[Persuadee] I'm always a little cautious about charities because of the stories you hear about all the money actually going to the CEOs.  This sounds like a pretty good charity though.  Do you think they are fiscally responsible?
[Persuader] good point. you never really know. but small donations hopefully make it to the right hands. how about 5 cents?
[Persuadee] You're right!  I would be willing to give $1.00 and then I'll investigate it more.
[Persuader] ok great thanks! have a nice weekend. i'll be praying for your health to improve.
[Persuadee] Thank you so much... you have a great weekend too!!
```
</details>

### 31. `20180903-133702_487_live`  —  old modifier: `deferred`

**Why:** Final line: "I'll donate half ($1.00). Good job!" - clear, specific, no hedge anywhere in the dialogue.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi!  I hope you are having a nice Holiday
[Persuadee] Yes and I hope yours is good also
[Persuader] I have a grown daughter and two precious grandchildren.  And you?
[Persuadee] WE just have a cat named Sissy. She's our child. LOL
[Persuader] WE have a dog named Bailey.  So including my husband I really have three children
[Persuadee] LOL, yeah they are like children. Bot pets and husbands.
[Persuader] Have you heard of the program Save the  Children?
[Persuadee] Yes, I saw an ad on TV recently about it.
[Persuader] It is a highly rated (88% out of 100%) program that provides health, education and emotional support for children around the world
[Persuadee] That's a lofty goal.
[Persuader] I agree, sometimes we have to break it down. .  You know, I am particularly interested in the children in Puerto Rico after Hurricane Maria.  They recently increased the death toll to over 3000.  But there is no breakdown for children
[Persuadee] Yes, they suffered greatly. there. But I'm more interested in what can be done for children in the US especially in the inner cities and Appalachia. 
[Persuader] Save the Children wrote and article called :The Urban Disadvantage.  It details what the call "The Survival of the Richest."  Save the Children has hundreds of low income clinics in cities are over American, and hundreds of outside educational programs to help urban children keep up.
[Persuadee] Oh that's really good to know. I thought they dealt mainly with ioverseas projects.
[Persuader] In the US, 1 out of 5 children are living in poverty.  Can you believe that, here in the US?  Save the Children was founded in 1932, and has provided services ever since.
[Persuadee] (Forgive my spelling mistakes! I need to proof before hitting send) I do believe that about the US. I used to work with inner city kids and know the horrors they live with here in the US.
[Persuader] The requester, Richard Kim has a 4/5 point rating.  He says the research team will collect all donations and send it to Save the Children. "How much do you like to donate to the charity now? Your donation will be directly deducted from your task payment. You can choose any amount from $0 to all your payment ($2) 
[Persuadee] You told me stuff I did not know about Save the Children. Because of that I'll donate half ($1.00). Good job!
[Persuader] Thank you.  I appreciate your generosity.
[Persuadee] Hey, I'm also the one that the cub and girl scouts mark my house cause I'm an easy touch esp where kids are concerned.
```
</details>

### 32. `20180903-135757_484_live`  —  old modifier: `deferred`

**Why:** "id be willing to donate .15 to the charity" - a decisive, specific-amount answer; no genuine hedge word (no maybe/might/probably) appears.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello friend  how are you today?
[Persuadee] i'm okay, how are you?
[Persuader] I am great thanks for asking. I am here to bring awareness to a great charity. Are you interested in hearing about it?
[Persuadee] sure, lets hear it. I'm all about charity 
[Persuader] Thats great well that charity is called Save the Children. Have you ever heard about it before?
[Persuadee] i haven't, can you tell me about it
[Persuader] Sure it is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries. 
[Persuadee] sounds very worthwhile, what kind of relief goes to the children
[Persuader] Relief includes food shelter education and safety. Are you interested in helping children achieve these important things?
[Persuadee] how much of the donation goes straight to the relief
[Persuader] 86 percent of the donation actually goes to helping the children. 9 percent gets reinvested into marketing for the charity at 5 percent into miscellaneous expenses.  As you can see much of the donation will go to helping these poor children. 
[Persuadee] id be willing to donate .15 to the charity
[Persuader] Wow that is a very kind gesture. This money would be collected from research team and they will send it to Save the Children
[Persuadee] okay thank you for that information, are you also going to donate?
[Persuader] Yes I plan on it. It warms my heart to bring a relief to children. Can you believe in this day and age children are still suffering?
[Persuadee] i can believe it, but that certainly doesn't mean it should continue. children are the last people that deserve any of this kind of life
[Persuader] I agree. There are millions of Syrian children that have grown up facing daily threat of violence. It needs to stop and hopefully Save the Children is an effort that can help. 
[Persuadee] if i could do anything in the world it would be peace, and that would be the first place id start, those poor children
[Persuader] As Whitney Houston once said  "I believe the children are our future  Teach them well and let them lead the way." No truer words have been spoken. Thanks again for your donation and sleep well knowing you did something to help.  
[Persuadee] thank you as well, the more people who get involved the better
```
</details>

### 33. `20180903-140806_586_live`  —  old modifier: `deferred`

**Why:** Explicitly finalized: "So 30 cents is your final donation for today?" / "Yes. I would like to donate 30 cents." Earlier hedges ("Maybe... I will probably donate late this year as well") concern a different, separate future year, not this final answer.

<details><summary>Full dialogue text</summary>

```
[Persuader] Do you want to help me make a difference?
[Persuadee] Sure
[Persuader] Have you heard of Save The Children, a well-acknowledged chairty?
[Persuadee] yes. I have donated before.
[Persuader] Would you like to donate again?
[Persuadee] Not sure why?
[Persuader] Children like Maria can use your help. She is one of ten children. They need all the help they can get. They live in a war zone.
[Persuadee] Oh that is horrible. I think I might donate. I think any amount of money will help. Are you going to donate?
[Persuader] I try to donate monthly. I will donate again this month. I think of how just a cup of coffee can pay for a meal for a family in another country like Maria.
[Persuadee] That is powerful. A little goes a long way for people in need. We may  not think much about a couple of bucks but to other people that can mean food for a day or two.
[Persuader] You're not donating just to the child but the family and helping them all.
[Persuadee] I think I could donate 25 cents. Will that be enough to help in some aspect? What is a general rule of thumb when making donations?
[Persuader] Ten cents is good. Twenty cents is better. 25 cents is better. But fifty cents can really help.
[Persuadee] I think I will stick with 25 cents. I usually try to stay consistent when making a effort to help others.
[Persuader] How about thirty cents?
[Persuadee] Ok. I can do 30 cents. I like to help other people less fortunate than me.
[Persuader] Do you think you can donate again next year too?
[Persuadee] Maybe. I am always open minded to helping other humans in need. I will probably donate late this year as well.
[Persuader] Ok. So 30 cents is your final donation for today?
[Persuadee] Yes. I would like to donate 30 cents. It is part of being a good human being.
```
</details>

### 34. `20180903-153105_741_live`  —  old modifier: `deferred`

**Why:** "I w[o]uld be willing to donate fifty cents" - decisive, specific figure, no hedge word.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi! How are you doing today?
[Persuadee] Hi, I'm good, just relaxing.  How are you
[Persuader] I am doing alright, thank you. I would like to talk to you about a charity. Do you donate at all?
[Persuadee] Yes I do some donating.
[Persuader] That is great, have you heard of save the children?
[Persuadee] I think so. Is that the one with the commercials f a man in another country with skinny children 
[Persuader] hm it might be, but it is an organization that raises money for children's rights to health, education, safety, etc. all around the world
[Persuadee] Ok well, I  think I  have heard of it but have not donated to this specific charity.
[Persuader] Woulld you be intrested in donating today? for the children?
[Persuadee] I would. Are you donating as well?
[Persuader] I may give a few cents. i am broke and its hard these days, but even a few cents can go a long way!
[Persuadee] Okay, well I can donate part of my earnings. Am I supposed to tell you how much?
[Persuader] Yes, how much would you like to donate today?
[Persuadee] I w9uld be willing to donate fifty cents.
[Persuader] That is very generous of you! the children will thank you
[Persuadee] Im more than happy to.
[Persuader] I thank you for your time and service today
[Persuadee] It was nice chatting with you. Have a good day!
[Persuader] You have a good day as well
[Persuadee] Im not sure what I am supposed to do now.
```
</details>

### 35. `20180903-165930_826_live`  —  old modifier: `deferred`

**Why:** "i'd be willing to contribute 50cents" - decisive, specific, no hedge word.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hello?
[Persuadee] hello. how's it going?
[Persuader] Not bad how are you?
[Persuadee] not too bad, how is your labor day going?
[Persuader] No complaints so far. Yours?
[Persuadee] pretty good. nice and lazy.
[Persuader] Yep same, this is about all the 'work' I've done all day.
[Persuadee] yeah. I worked most of the day, but at a pretty slow pace
[Persuader] Right on. So back to 'work'. I was wondering if you would be interested in donating a portion of your payment from this task towards a charity called Save the Children
[Persuadee] i'm familiar with them. how efficient are they as a charity though?
[Persuader] Save the Children is extremely efficient. Well as efficient as a charity can be on a count of the donations they receive. Save the Children is not like some other charities you may hear about that have a handsomely paid CEO with small minuscule percentages going to help the needy. 
[Persuadee] i'd be willing to contribute 50cents
[Persuader] That's so kind of you thank you.
[Persuadee] ok cool. do you work for them? or just voluteering?
[Persuader] I'm just volunteering for the time being. Myself, like many others who help with Save the Children, volunteer our time for no pay or compensation.
[Persuadee] that is really great. more people should do that.
[Persuader] You learn a lot about people when you put yourself in this sort of position. I know I feel like a better person for volunteering.
[Persuadee] how long have you been doing that, and how did you get involved?
[Persuader] I've only started recently. My wife and I discussed doing something for other people as a way for the two of us to spend time together. It's a way for us to feel productive or useful in contrast to our normal boring shut-in selves.
[Persuadee] heheheh. I've always wanted to do volunteer work, but don't really know where to get started.
[Persuader] Give it a try sometime I don't think you'll regret it.
```
</details>

### 36. `20180903-165952_124_live`  —  old modifier: `deferred`

**Why:** "Sure, I can give 0.50 to the save the children organization." Unhedged. The separate agreement to "look at" the charity's website for future consideration doesn't qualify the $0.50 already given.

<details><summary>Full dialogue text</summary>

```
[Persuader] Willyou consider finding part of your hot payment t_ charity?
[Persuadee] It depends on the charity and whether or not I think it's a good cause. 
[Persuader] Totally fair.  I hoped you'd say that because people who care where the money goes will love helping children with Save The Children
[Persuadee] Do you know any more about the charity? What exactly do they do?
[Persuader] For starters,  they are an international organization (non-governmental) that promotes children's rights
[Persuadee] What kinds of things do they do to promote children's rights? Where does the money go when it is sent to that charity?
[Persuader] Here's the good part: the turk researchers collectthe money from the hits and sendit directly t_ the charity.  Ther problem is,  so many kids are in war zones,  food deserts,  and other tough areas.  Save The Children is there t_ defend them
[Persuadee] I get that, and I think it's great, but I am just very careful who I donate to. So how do they defend them? 
[Persuader] One thing they do is build shelters sothey havea place to live.   That alone is a near miracle for so many of these kids.  Hey,  check this site out  URL 
[Persuadee] Do you know if they provide a way for the next generation of these children to get out of poverty and the poverty mindset? Like instead of giving someone a fish for dinner, teach them how to fish sort of thing?
[Persuader] Gh ets the first step for a charity likethis.  When kids are fed and sheltered theyare healthy.  That lets them learn.  So,  Save The Children had literacy and learning programs they use with the kids
[Persuadee] That's great. It sounds similar to an organization I've been donating to for over a decade. Have you ever heard of Compassion International?
[Persuader] Yes!  I considered a child through them for several years.  I used to send him Christmas presents and such aloooong with monthly donations.   The two charities are very similar
[Persuadee] That's wonderful. I actually sponsor three children through them now. Two years ago I was able to go and visit one of the girls I sponsor in Peru. It was the most surreal experience and made it so much more real seeing how my money had helped her life. I also got to see firsthand what the organization does with the children. 
[Persuader] That is awesome!  Experiences like that are great for the giver and the kids.   It's sad t_ see what they have to deal with even after help, many times.  You've seen this first hand so you probably wouldn't have any problem with giving STC 0.50 from the hit payment,  right?
[Persuadee] Sure, I can give 0.50 to the save the children organization.
[Persuader] That's very niceof you!  I appreciate that.   It's a cliche but it's true,  0.50 doesn't mean much to us but it really does matter for these kids. 
[Persuadee] I agree with that. It goes a long way in another country. 
[Persuader] Yes!  I know you already sponsor,  but would you look at the STC website and consider donating to them in ther future?  It seems like everyone wantsto helpbut thre is a lot more need than funds
[Persuadee] I will agree to look at it, sure. 
[Persuader] Thank you so much.  I hope that youget to see all of your donations meet needs no matter who theyare to.  Thank you for the donations you've made ti sponsor ids already.  No matter whothe donationsgo through, the kids really benefit!
```
</details>

### 37. `20180903-172112_282_live`  —  old modifier: `deferred`

**Why:** Resolves cleanly after hedging earlier ("I am not sure if I will do that"): final line is "I believe that I will donate ten cents" - a decisive statement, not a doubt.

<details><summary>Full dialogue text</summary>

```
[Persuader] Hi how are you?
[Persuadee] I am great!  How about you?
[Persuader] I'm ok...been a very hot day...glad to be inside.  Do you have time for me to tell you about a charity I like?
[Persuadee] I sure do!
[Persuader] Great.  I like this charity called Save the Children.  Have you heard of them?
[Persuadee] I think that I have seen ads on tv for it.  It helps impoverished children in developing countries, I believe.
[Persuader] Yes they help children in developing countries with a lot of different things.   It's surprising how much less these children have.
[Persuadee] Yes, I think they do a lot of good.  Do you donate to them?
[Persuader] I do donate to them.  Do you donate to any charities?
[Persuadee] I donate occasionally.  I did last year after the devastating hurricanes that hit the south.  Houston, specifically.
[Persuader] Yeah I always have certain charities that speak to me.  You are able to donate a portion of your earning from this to Save the Children if they interest you.
[Persuadee] Hmm, I am not sure if I will do that.  It is tough to know if a little bit would make any difference.
[Persuader] Any little bit helps...if everyone gives even 10 cents, that adds up.
[Persuadee] What would you do?
[Persuader] I like to donate a little bit when I'm asked.  Especially since it's tax deductible.
[Persuadee] That is good to know!  I do forget that I can deduct charitable contributions.  I am thinking I may donate a little.
[Persuader] Yeah and making small donations throughout the year adds up...makes a good tax deduction.
[Persuadee] Okay, then.  I believe that I will donate ten cents.
[Persuader] That's great!  You can always read up on them to see where your donation will go.  Over 80% of it goes directly to helping the children.
[Persuadee] Thank you for your suggestion!  I am happy to support a good cause, and 80% seems like a pretty substantial portion of the actual pool of donations.
```
</details>

