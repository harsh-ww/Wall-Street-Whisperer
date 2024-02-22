from NewsSentiment import TargetSentimentClassifier
tsc = TargetSentimentClassifier()

data = [
(
    "", "Amazon" , " has been fined €32m (£27m) in France for excessive surveillance of its workers, including measures the data watchdog found to be illegal. The CNIL said Amazon France Logistique, which manages warehouses, recorded data captured by workers' handheld scanners. It found Amazon tracked activity so precisely that it led to workers having to potentially justify each break. Amazon said it strongly disagreed with the CNIL's findings and called them \"factually incorrect\". France's data protection agency investigated Amazon warehouses following complaints by employees as well as media coverage of conditions. It outlined a number of areas where it found Amazon had breached General Data Protection Regulation (GDPR). This included a system with three alerts in place to monitor employee activity, which the CNIL ruled to be illegal. One alert triggered if an item was scanned too quickly or less than 1.25 seconds after scanning a previous item, increasing the risk of error. Another signalled breaks of 10 minutes or more, while a third tracked breaks between one and 10 minutes. The CNIL also questioned why Amazon needed to keep workers' data for 31 days. Responding to the findings an Amazon spokesperson said: \"We strongly disagree with the CNIL's conclusions which are factually incorrect and we reserve the right to file an appeal. Warehouse management systems are industry standard and are necessary for ensuring the safety, quality, and efficiency of operations and to track the storage of inventory and processing of packages on time and in line with customer expectations.\""
)
]

sentiments = tsc.infer(targets=data)

for i, result in enumerate(sentiments):
    print("Sentiment: ", i, result[0], result)
