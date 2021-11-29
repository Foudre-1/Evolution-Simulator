def handle_one():
  print("A")

def handle_two():
  print("B")

def handle_three():
  print("C")


{'one': handle_one, 
 'two': handle_two, 
 'three': handle_three}["one"]()