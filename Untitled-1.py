name = input ("enter your name")

with open('guest.txt' , 'w') as f:
 f.write(name)

 while True:
    name == input("enter your name")
    if name == "quit":
      break

    print(f"Hello {name}, adding you.")
    with open('guest.txt' , 'a') as f:
      f.write(name + "\n")   


      while True:
        reason = input("why are you visiting? or type 'quit' to exit")
        if reason == "quit":
          break

        with open('reasons.txt' , 'a') as f:
          f.write(reason + "\n")