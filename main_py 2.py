# task - make a voting system with login credentials

def login_credential():
      name = input("enter your name : ")
      country = input("enter your country :")


      if country == "india" :
            print("you are allowed to vote here")
      else:
            print("you are not allowed to vote here")

      age = int(input("enter your age :"))

      if age == 18 :
            print("you are allowed to vote here")
      else :
            print("you are not allowed to vote here")


      print("message from the system - it will allow you to vote if you are above 18")

      print("you are welcomed to vote here "
            "note - this system is runed by the election commision of india ")

def voting ():
      question = input("enter a question :")
      answer = input("enter the correct answer : ")
      logic = input("enter the logic of the correct answer : ")

      if logic == str :
            print(" ")
      else:
            print("the question is out of range")

            option_a = input("option a :")
            option_b = input("option b :")
            option_c = input("option c :")
            option_d = input("option d :")

            print("select one option from above ")

            options = input("enter the letter of your answer")
            print("you have selected ",options)

            if options == answer:
                  print("your answer is correct")
            else :
                  print ("your answer is wrong")
                  print("keep going you'll do it")
                  print (logic)

login_credential()
voting()
