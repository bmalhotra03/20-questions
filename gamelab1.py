# Author: Brij Malhotra
# Filename: gamelab1.py
# Version: 1
# Purpose: Program simulates a 20 questions class game

import sys

# Define tree node class
class TreeNode:
    def __init__(self, node_id, node_type, value, parent_id=None, left_child=None, right_child=None):
        self.node_id = node_id
        self.node_type = node_type
        self.value = value
        self.parent_id = parent_id
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return f"{self.node_type} Node(ID: {self.node_id}, Value: {self.value})"

# Parse through the input tree file and assign node structure values accordingly
def parse_treefile(filepath):
    
    # Error handling to see if file was loaded and read properly
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
    # This will void the treefile and let user start the game themselves by providing the first question
    except:
        print("Error loading the tree file, please try again!\n")
        return None, []
    
        
    # Variable to initialize list size based on number of nodes   
    maxVal = 0
    
    # Go through each node value and compare with maxVal
    for line in lines:
        val = int(line.split(':')[0])
        if maxVal < val:
            maxVal = val
    
    # Initialize empty list with size maxVal   
    nodes = [None] * (maxVal + 1)           

    # This is where the parsing is done
    for line in lines:
        
        # Parse through the file to get fields to set the treenode
        parts = line.strip().split(':')
        
        # Error check to see if enough fields are there for the program to initialize
        # a tree node based on the tree file
        if len(parts) < 6:
            continue
        
        # Initialize the values based off the parsing
        node_id = int(parts[0])
        node_type = parts[1]
        value = parts[2]
        parent_id = None if parts[3] == 'None' else int(parts[3])
        left_child = None if parts[4] == 'None' else int(parts[4])
        right_child = None if parts[5] == 'None' else int(parts[5])

        # Create the tree node object
        nodes[node_id] = TreeNode(node_id, node_type, value, parent_id, left_child, right_child)
    
    # Navigating the tree and setting the left and right child
    for node in nodes:
        if node is not None:
            if node.left_child is not None:
                node.left_child = nodes[node.left_child]
            if node.right_child is not None:
                node.right_child = nodes[node.right_child]
    
    # Finding the root
    root = next((node for node in nodes if node and node.parent_id is None), None)
    return root, nodes

def play_game(curr, nodes):
    
    # Question number count because this is 20 questions after all
    question_count = 0
    
    while curr and (question_count < 20):
        
        # Increment question counter
        question_count += 1
        
        # Check if the current node is a question node
        if curr.node_type == 'question':
            # Prompt question and retrieve the input
            response = input(f"{curr.value} (y/n): ")
            # Navigate the tree based on input
            curr = curr.left_child if response.lower() == 'y' else curr.right_child
        else:
            # Current node is an answer, user has to answer the guess
            guess = input(f"Is it a(n) {curr.value}? (y/n): ")
            if guess.lower() == 'y':
                # Break from loop if program quesses correctly
                print("I win! Better luck next time.")
                break
            else:
                # This is where the learning and addition of the tree is implemented
                print("You've stumped me! Help me learn how to beat you next time.")
                item = input("What were you thinking of? ")
                
                # Get new question
                question = input(f"Give me a new yes/no question that would distinguish {item} from {curr.value}: ")
                if_yes = input(f"Would a(n) {item} be associated with a yes or no answer to your new question? (y/n): ")
                
                # Create new question and answer node based on the input from user above
                new_question_id = len(nodes)
                new_answer_id = new_question_id + 1
                new_question = TreeNode(new_question_id, 'question', question)
                new_answer = TreeNode(new_answer_id, 'answer', item)
                
                # Add new nodes to the nodes list
                nodes.append(new_question)
                nodes.append(new_answer)
                
                # Link the new nodes correctly
                if if_yes.lower() == 'y':
                    new_question.left_child = new_answer
                    new_question.right_child = curr
                else:  
                    new_question.right_child = new_answer
                    new_question.left_child = curr
                    
                # Link the question to the tree based on its association
                if curr.parent_id is not None:
                    parent_node = nodes[curr.parent_id]
                    if parent_node.left_child == curr:
                        parent_node.left_child = new_question
                    else:
                        parent_node.right_child = new_question
                new_question.parent_id = curr.parent_id

                # New question is added and game will add it via the learning implementation
                curr.parent_id = new_question_id
                break
            
    # Check to see if the program ran out of questions or not
    if question_count >= 20:
        print("I've run out of questions! You win!")

    if input("Play again? (y/n): ").lower() == 'y':
        play_game(nodes[0], nodes)  # Restart from the root node

if __name__ == "__main__":
    root = None
    nodes = []
    # Take the treefile via the commandline argument and then parse to set the root
    if len(sys.argv) > 1:
        root, nodes = parse_treefile(sys.argv[1])
    
    # Initialize the tree if no valid file is provided or the file is empty
    if root is None:
        question = input("No tree file found. Provide the first question: ")
        answer = input("What's an example answer for 'yes' to your question? ")
        root = TreeNode(0, 'question', question)
        yes_node = TreeNode(1, 'answer', answer)
        no_node = TreeNode(2, 'answer', 'Not known yet')
        root.left_child = yes_node
        root.right_child = no_node
        nodes.extend([root, yes_node, no_node])
       
    # Start game :D 
    play_game(root, nodes)