# kazakh_lexicon
Process a json file with kazakh setences and extract lemmas and related information from it.

## Libraries
Pydantic library is required to run the file.
You can install pydantic with the following command:

```pip install pydantic```

## Running the code
The script expects a file named ```sample_parsed_sentences.json``` in the same directory as the code.
The output is written to a ```lemma_lexicon.json``` file in the same directory.

## Running in Production Environment
The cloud infrastructure that we run this code on would depend on the use cases and also the size and scale of the data we are dealing with. I've worked with Azure cloud before and I'd like to explain my reasoning with examples based on Azure. If it is a simple file with a few thousand sentences and tens of thousands of lemmas, running it on-premises might be faster and cheaper than using cloud resources. A good laptop should be able to handle this kind of processing.

But if the text we have to process is in the order of millions or even billions of sentences taken from across the internet, we would need to go with a distributed system. One way to do this would be to deploy multiple instances of this script as Azure functions, each running independently. Because the processing is now distributed we would have to distribute the data as well and make sure it is accessible to all the Azure functions. Another thing to take care of would be to distribute the processing across Azure functions so that there is no redundancy in the calculations. We would store all the data in a database and then make each Azure function read only a unique part of this database. For example, instance 1 would read rows 1 through 1000, instance 2 would read 1001 through 2000 and so on. Once all the functions have finished processing the sentences and have a list of lemmas, they would then write to the database into a new table that holds the lemma entries. Each function would search for that lemma in the table and update information for it, for example by increasing the frequency column. If the lemma doesn't exist we would add a new entry. The database will make sure that our operations are atomic and that the data is in a valid state.

Another advantage of deploying on the cloud can be seen when this process of collecting lemmas is an online one. For example, we might have a crawler (again deployed on the cloud, maybe with multiple instances) that continuously crawls the internet for Kazakh sentences and adds them to our database. Our Azure functions would periodically check the database for new entries and then process these sentences. Alternatively, we could push the messages to a queue (kafka, message queue in Azure) and the functions can then read from this queue. We can also scale the instances of the Azure functions based on the number of messages that are pending in the queue to save on costs.

## Design Details
My initial thought was to have a dictionary of lemmas and use lemma text as the key to make sure I had a list of all the unique lemmas. But on looking closely at the data I noticed that the lemma 'кейбір' shows up with two different POS, as a DET and an ADJ. So instead I'm using a combination of both lemma text and POS as the key to store the lemmas (in addition to having unique ids). The reason for this is that while the words 'bat' (like a cricket bat) and 'bat' (like the animal) both have 'bat' as the lemma text, they have completely different meanings. Adding POS avoids this confusion, at least in this dataset. I've also used data classes as asked in the task to store the lemmas instead of the pydantic recommended 'BaseModel'.
