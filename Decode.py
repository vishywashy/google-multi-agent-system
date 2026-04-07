from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
print(tokenizer.decode([101, 1037, 20917, 4014, 4005, 4490, 2004, 1037, 2958, 1010, 7176, 2536, 4007, 3454, 2083, 1996, 20917, 4014, 2326, 102]))