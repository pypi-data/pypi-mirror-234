import argparse
import os
import readline
import re
import subprocess
import threading
from typing import List, Optional, Tuple, Union
import torch
from termcolor import cprint, colored
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer, logging as trans_log
import logging
from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.analysis import StandardAnalyzer
import random
import time
import importlib.resources as resources
from spellchecker import SpellChecker


trans_log.set_verbosity_error()
analyzer = StandardAnalyzer(stoplist=None)
schema = Schema(title=TEXT(stored=True, analyzer=analyzer),
                path=ID(stored=True),
                content=TEXT(stored=True, analyzer=analyzer))
logging.basicConfig(filename='command_errors.log', level=logging.ERROR)


class InteractiveGenerator:
    IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    FLAG_PATTERN = re.compile(r'(-\w+|--[\w-]+)')  # Updated Regular expression
    URL_PATTERN_VALIDATION = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'





    def __init__(self):
        self.args = self._parse_arguments()
        self.index_dir = self.return_path("indexdir")
        self.s3_url = self._determine_s3_url()
        self.command_history = self._get_command_history()
        self._ensure_model_folder_exists()
        self._validate_model_dirs()
        self.command_running = False
        self._ensure_results_directory_exists()
        self.max_truncate_length: int = 500
        self.current_model_name= self._load_tokenizer_and_model()
        self.always_apply_action: bool = False
        self.print_lock = threading.Lock()
        self.services = []
        self.print_star_sky()
        self.flag_file = self.return_path(self.current_model_name+"_flags")
        self.flag_descriptions = self._load_flag_descriptions(self.flag_file)
        self.extracted_flags = []
        

    def print_farewell_message(self, width=30, height=10, density=0.5):
        # Calculate the position to print the farewell message
        farewell_msg = "Until our stars align again!!"
        start_x = (width - len(farewell_msg)) // 2
        start_y = height // 2
        
        star_colors = ["cyan", "magenta", "yellow", "blue"]  # Nebula-themed colors for stars

        for y in range(height):
            for x in range(width):
                # Check if we are at the position to print the farewell message
                if y == start_y and start_x <= x < start_x + len(farewell_msg):
                    print(colored(farewell_msg[x - start_x], 'green', attrs=['bold']), end='')
                    continue

                if random.random() < density:
                    chosen_star = '*' if random.random() < 0.5 else '.'
                    print(colored(chosen_star, random.choice(star_colors)), end='')
                else:
                    print(' ', end='')
            print()  # Move to the next line after each row
    def print_star_sky(self, width=30, height=10, density=0.5):
        # Calculate the position to print the welcome message
        welcome_msg = "Welcome to Nebula"
        start_x = (width - len(welcome_msg)) // 2
        start_y = height // 2
        
        star_colors = ["cyan", "magenta", "yellow", "blue"]  # Nebula-themed colors for stars

        for y in range(height):
            for x in range(width):
                # Check if we are at the position to print the welcome message
                if y == start_y and start_x <= x < start_x + len(welcome_msg):
                    print(colored(welcome_msg[x - start_x], 'green', attrs=['bold']), end='')
                    continue

                if random.random() < density:
                    chosen_star = '*' if random.random() < 0.5 else '.'
                    print(colored(chosen_star, random.choice(star_colors)), end='')
                else:
                    print(' ', end='')
            print()  # Move to the next line after each row

    @staticmethod
    def _parse_arguments():
        parser = argparse.ArgumentParser(description='Interactive Command Generator')
        parser.add_argument('--results_dir', type=str, default='./results', help='Directory to save command results')
        parser.add_argument('--model_dir', type=str, default='./unified_models', help='Path to the model directory')
        return parser.parse_args()

    def _load_flag_descriptions(self, file_path):
        """Load flag descriptions from a file and return them as a dictionary."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
            # Store the entire line as the value in the dictionary using flag as key
            return {line.split(":")[0].strip(): line.strip() for line in lines if ":" in line}

    def extract_and_match_flags(self, command):
        """Extract flags from the command and match them with descriptions."""
        flags = self.FLAG_PATTERN.findall(command)
        
        # Using set comprehension to ensure uniqueness
        matched_descriptions = list({self.flag_descriptions[flag] for flag in flags if flag in self.flag_descriptions})
        
        self.extracted_flags.extend(matched_descriptions)
        return matched_descriptions

    
    def return_path(self, path):
        if self.is_run_as_package():
            print("Running as PYPI package, setting appropriate paths")
            with resources.path('nebula', path) as correct_path:
                return str(correct_path)
        return path


    @staticmethod
    def _determine_s3_url():
        return "https://nebula-models.s3.amazonaws.com/unified_models_no_zap.zip" if os.environ.get('IN_DOCKER') else "https://nebula-models.s3.amazonaws.com/unified_models.zip"

    def _get_command_history(self):
        if os.path.exists(self.args.results_dir):
            return [(file, os.path.join(self.args.results_dir, file)) for file in os.listdir(self.args.results_dir) if file.startswith("result_")]
        return []

    def _ensure_model_folder_exists(self):
        if not self.folder_exists_and_not_empty(self.args.model_dir):
            print(f"{self.args.model_dir} not found or is empty. Downloading and unzipping...")
            self.download_and_unzip(self.s3_url, f"{self.args.model_dir}.zip")
        else:
            print(f"{self.args.model_dir} already exists and is not empty.")

    def _validate_model_dirs(self):
        model_dirs = [d for d in os.listdir(self.args.model_dir) if os.path.isdir(os.path.join(self.args.model_dir, d))]
        if not model_dirs:
            raise ValueError("No model directories found in the specified directory.")

    def _ensure_results_directory_exists(self):
        if not os.path.exists(self.args.results_dir):
            os.makedirs(self.args.results_dir)

    

    def is_run_as_package(self):
    # Check if the script is within a 'site-packages' directory
        return 'site-packages' in os.path.abspath(__file__)

    def folder_exists_and_not_empty(self, folder_path):
        # Check if the folder exists
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return False
        # Check if the folder is empty
        if not os.listdir(folder_path):
            return False
        return True

    def download_and_unzip(self, url, output_name):
        try:   
            # Download the file from the S3 bucket using wget with progress bar
            print("Downloading...")
            subprocess.run(['wget', '--progress=bar:force:noscroll', url, '-O', output_name])

            # Create the target directory if it doesn't exist
            target_dir = os.path.splitext(output_name)[0]
            os.makedirs(target_dir, exist_ok=True)

            # Unzip the downloaded file to the target directory
            print("\nUnzipping...")
            subprocess.run(['unzip', output_name, '-d', target_dir])

            # Remove the zip file (optional)
            os.remove(output_name)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


    def _load_tokenizer_and_model(self) -> None:
        self.tokenizers = {}  # Dictionary to store all tokenizers
        self.models = {}     # Dictionary to store all models
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Set the device once

        # Iterating over each model directory
        for model_folder in os.listdir(self.args.model_dir):
            full_path = os.path.join(self.args.model_dir, model_folder)
            
            # Check if it's a directory to avoid loading from non-directory paths
            if os.path.isdir(full_path):
                try:
                    # Load tokenizer
                    cprint(f"Loading tokenizer for {model_folder}...", 'yellow', end='', flush=True)
                    tokenizer = GPT2Tokenizer.from_pretrained(full_path)
                    cprint(" Done!", 'green')

                    # Load model
                    cprint(f"Loading model for {model_folder}...", 'yellow', end='', flush=True)
                    model = GPT2LMHeadModel.from_pretrained(full_path)
                    model.eval()
                    try:
                        model.to(self.device)
                    except Exception:
                        cprint(f"Warning: Unable to move the model to the specified device ({self.device}). Defaulting to CPU.", 'yellow')
                        self.device = torch.device("cpu")
                        model.to(self.device)

                    cprint(" Done!", 'green')
                    
                    # Add the successfully loaded model and tokenizer to their respective dictionaries
                    self.tokenizers[model_folder] = tokenizer
                    self.models[model_folder] = model
                    
                except Exception as e:
                    cprint(f"Failed to load model/tokenizer from {model_folder}: {e}", 'red')

        # Setting the "current" tokenizer and model to the first one loaded, for immediate use
        if self.tokenizers and self.models:
            first_loaded = list(self.tokenizers.keys())[0]
            self.current_tokenizer = self.tokenizers[first_loaded]
            self.current_model = self.models[first_loaded]
            
            # Inform the user about the current model in use
            cprint(f"\nThe current model in use is: {first_loaded}\n", "blue")

        return first_loaded

    def run_command_and_alert(self, text: str) -> None:
        """
        A function to run a command in the background, capture its output, and print it to the screen.
        """

        def execute_command(command: Union[str, List[str]]) -> Tuple[int, str, str]:
            """
            Executes the provided command and returns the returncode, stdout, and stderr.
            """
            try:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
                stdout, stderr = process.communicate()
                
                # Reset the terminal to a sane state after subprocess execution
                os.system('stty sane')
                
                return process.returncode, stdout, stderr
            except Exception as e:
                logging.error(f"Error while executing command {command}: {e}")
                return -1, "", str(e)

        print("\nExecuting command, you can choose the view previous command option in the main menu to view the results when command execution has been completed")

        if isinstance(text, list):
            command_str = ' '.join(text)
        else:
            command_str = text

        # Execute the command
        returncode, stdout, stderr = execute_command(command_str)

        truncated_cmd = command_str[:15].replace(' ', '_') + ('...' if len(command_str) > 15 else '')
        result_file_path = os.path.join(self.args.results_dir, f"result_{truncated_cmd}_{len(self.command_history) + 1}.txt")

        with open(result_file_path, 'w') as f:
            if returncode == 0:
                f.write(stdout)
            else:
                print("\nCommand Error Output:")
                print(stderr)
                f.write(stderr)
                logging.error(f"Command '{command_str}' failed with error:\n{stderr}")

        # Update command history
        self.command_history.append((text, result_file_path))



    @staticmethod
    def ensure_space_between_letter_and_number(s: str) -> str:
        try:
            if not isinstance(s, str):
                raise ValueError("The input must be a string.")

            # Regex operations
            # Match everything up to the first colon that's not immediately followed by a MAC address or an IP address
            s = re.sub(r'^.*?:\s(?!(?:[0-9a-fA-F]{2}:)+)(?!\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', '', s)

            s = re.sub(r'-(?=\d)', '', s)
            s = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', s)
            s = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', s)
            s = re.sub(r'\.$', '', s)

            return s.strip()

        except Exception as e:
            print(f"Error in ensure_space_between_letter_and_number: {e}")
            return s




    @staticmethod
    def _extract_ip(s: str) -> Optional[str]:
        """
        Extracts the first IP address found in the given string based on a pattern.
        If no IP address is found, it returns None.
        """
        try:
            ips = InteractiveGenerator.IP_PATTERN.findall(s)
            return ips[0] if ips else None
        except Exception as e:
            logging.error(f"Error while extracting IP from string '{s[:30]}...': {e}")
            return None

    def process_string(self, s: str, replacement_ips: list, replacement_urls: list) -> str:
        """Replace the IP addresses and URLs in the given string with the respective replacements."""

        

        try:
            if not isinstance(s, str):
                raise ValueError("The input string must be a string.")
        except Exception as e:
            logging.error(f"Error in input string validation: {e}")
            
        try:
            for ip in replacement_ips:
                if not re.match(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', ip):
                    raise ValueError(f"One of the replacement IPs ({ip}) is not valid.")
            ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            ip_addresses = re.findall(ip_pattern, s)
            if ip_addresses:
                for i, ip in enumerate(ip_addresses):
                    if i < len(replacement_ips):
                        s = s.replace(ip, replacement_ips[i])
        except Exception as e:
            logging.error(f"Error in IP processing: {e}")

        # Validate URLs in replacement_urls list
        try:
            for url in replacement_urls:
                if not re.match(self.URL_PATTERN_VALIDATION, url):
                    raise ValueError(f"One of the replacement URLs ({url}) is not valid.")
        except Exception as e:
            logging.error(f"Error in URL validation: {e}")

        # Extract and replace URLs
        try:
            if replacement_urls:
                urls = self.extract_urls(s)
                for i, url in enumerate(urls):
                    if i < len(replacement_urls):
                        s = s.replace(url, replacement_urls[i])
        except Exception as e:
            logging.error(f"Error in URL processing: {e}")

        return s

        
    def extract_urls(self, s: str) -> list:
        """Extract URLs from the given string.

        Args:
            s (str): The input string.

        Returns:
            list: List of URLs found in the string.
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, s)
    
    def generate_text(self, prompt_text: str, max_length: int = 300000) -> str:
        """
        Generate text using the current model based on the provided prompt.
        
        Parameters:
        - prompt_text: Initial text to prompt the model for generation.
        - max_length: Maximum length for the generated text.
        
        Returns:
        - The generated text as a string.
        """
        try:
            if len(prompt_text) > self.current_model.config.n_ctx:
                logging.warning("Prompt too long! Truncating...")
                print("Prompt too long! Truncating...")
                prompt_text = prompt_text[:self.current_model.config.n_ctx]

            encoding = self.current_tokenizer.encode_plus(
                prompt_text,
                return_tensors="pt",
                add_special_tokens=True,
                max_length=max_length,
                pad_to_max_length=False,
                return_attention_mask=True,
                truncation=True
            )

            input_ids = encoding["input_ids"].to(self.device)
            attention_mask = encoding["attention_mask"].to(self.device)

            with tqdm(total=max_length, desc="Generating text", position=0) as pbar:
                output = self.current_model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_length=max_length,
                    num_return_sequences=1,
                    do_sample=True,
                    top_k=40,
                    top_p=0.95,
                    temperature=0.1,
                    repetition_penalty=1.0
                )
                pbar.update(len(output[0]))

            generated_text = self.current_tokenizer.decode(output[0], skip_special_tokens=True)

            return generated_text

        except Exception as e:
            logging.error(f"Error during text generation with prompt '{prompt_text[:30]}...': {e}")
            return ""  # Returning an empty string as a fallback. Adjust based on your requirements.


    def start_interactive_mode(self) -> None:
        """
        Start an interactive session for the user to input prompts and receive generated text.
        
        In the interactive session:
        - The user is prompted to enter text.
        - The model generates text based on the user's input.
        - The generated text is displayed and handled accordingly.
        - The session can be exited by typing 'exit' or through keyboard interrupts.
        """
        print("Enter 'exit' to quit the interactive mode.")
        
        while True:
            try:
                prompt = self.get_user_prompt()
                
                if prompt.lower() == 'view_results': 
                    still_viewing = self._view_previous_results()
                    if still_viewing:
                        continue
                    else:
                        print("Returning to the main prompt.")
                        continue

                if not prompt:
                    print("Prompt is empty. Please enter a valid prompt.")
                    continue

                if prompt.lower() == 'exit':
                    break

                generated_text = self.generate_and_display_text(prompt)
                self.handle_generated_text(generated_text)

            except (EOFError, KeyboardInterrupt):  # Combined the two exception types
                self.print_farewell_message()
                break
            except Exception as e:  # Handle unexpected errors
                if isinstance(prompt, bool):
                    logging.error(f"Error during interactive session with prompt '{prompt}...': {e}")
                elif isinstance(prompt, list):
                    logging.error("prompt value is:%s", prompt)
                    logging.error(f"Error during interactive session with prompt '{prompt[:30]}...': {e}")


    def display_command_list(self) -> None:
        """
        Display a list of previously executed commands truncated to self.max_truncate_length.
        """
        cprint("\nPrevious Commands:", "cyan")
        for idx, (command, _) in enumerate(self.command_history):
            truncated_cmd = (command[:self.max_truncate_length] + '...') if len(command) > self.max_truncate_length else command
            print(f"{idx+1}. {truncated_cmd}")

    def get_user_prompt(self) -> str:
        """
        Interactively prompt the user for an action or command input.
        
        Returns:
            str: The user's command input.
        """
        try:
            # If there's a command currently running, offer to wait for it
            if self.command_running:
                action = input(colored("\nA command is currently running. Do you want to (w) wait for it to complete, or (c) continue without waiting? [w/c]: ", "cyan")).strip().lower()
                if action == 'w':
                    print("Waiting for the command to complete...")
                    while self.command_running:
                        time.sleep(1)  # Check every second
                    print("Command completed!")
                    return


            action = input(colored("\nDo you want to (c) enter a new command, (v) view previous results, (pr) process previous nmap results,\n(m) select a model, (s) to search by keywords or (q) quit? [c/v/m/q]: ", "cyan")).strip().lower()

            # Handle the user's action
            if action == 'q':
                self.print_farewell_message()
                exit(0)
            elif action == 'v':
                return self._view_previous_results()
            elif action == 'pr':
                return self._process_previous_nmap_results()
            elif action == 'c':
                return self._input_command_without_model_selection()
            elif action == 'm':
                self._select_model()  # A new private method to select a model
                return self._input_command_without_model_selection()  # Return to the main menu after selecting a model
            elif action == 's':
                return self.user_search_interface()
            else:
                cprint("Invalid option. Please choose either 'c', 'v', 'm', or 'q'.", "red")
                return self.get_user_prompt()

        except Exception as e:  # Handle unexpected errors
            logging.error(f"Error during user prompt: {e}")
            cprint("An unexpected error occurred. Please try again.", "red")
            return self.get_user_prompt()

    def _select_model(self) -> None:
        """
        Interactively allows the user to select a model from the available models.
        """
        try:
            # Displaying available models
            model_names = list(self.tokenizers.keys())
            for idx, model_name in enumerate(model_names, 1):
                print(f"{idx}. {model_name}")

            while True:
                choice = input(colored("\nSelect a model by entering its number: ", "cyan")).strip()
                
                if choice.isdigit() and 1 <= int(choice) <= len(model_names):
                    selected_model_name = model_names[int(choice) - 1]
                    index_of_choice = list(self.tokenizers.keys())[int(choice) - 1]
                    self.current_model = self.models[index_of_choice]
                    self.current_tokenizer = self.tokenizers[selected_model_name]
                    if selected_model_name == "nmap":
                        self.flag_file=self.return_path("nmap_flags")
                    
                    elif selected_model_name == "crackmap":
                        self.flag_file=self.return_path("crackmap_flags")

                    elif selected_model_name == "nuclei":
                        self.flag_file=self.return_path("nuclei_flags")

                    elif selected_model_name == "zap":
                        self.flag_file=self.return_path("zap_flags")
                    self.flag_descriptions = self._load_flag_descriptions(self.flag_file)
                    cprint(f"You've selected the {selected_model_name} model!", "green")
                    break
                else:
                    cprint("Invalid choice. Please enter a valid number.", "red")

                    
        except Exception as e:
            logging.error(f"Error during model selection: {e}")
            cprint("An unexpected error occurred during model selection. Please try again.", "red")


    def _input_command(self) -> str:
        """Internal method to get a command input from the user."""
        
        # Prompt the user if they want to change the model or proceed
        choice = input(colored("\nDo you want to (p) proceed with the current model, (m) select a different model, or (q) quit? [p/m/q]: ", "cyan")).strip().lower()

        if choice == 'q':
            self.print_farewell_message()
            exit(0)
        elif choice == 'm':
            self._select_model()  # Assuming you have a method _select_model to handle model selection
            return self._input_command_without_model_selection() # Recursively call this method to get user input again after changing model
        elif choice != 'p':
            print("Invalid choice. Defaulting to proceed with the current model.")

        # Get the actual user input for the model to generate
        user_input = input(colored("\nEnter a prompt: ", "cyan")).strip()
        if user_input.lower() in ['quit', 'exit']:
            self.print_farewell_message()
            exit(0)
        return user_input


    def _input_command_without_model_selection(self) -> str:
            """Internal method to get a command input from the user without model selection."""
            
            # Initialize the spell checker
            spell = SpellChecker()
            
            # Get the actual user input for the model to generate
            user_input = input(colored("\nEnter a prompt: ", "cyan")).strip()
            
            # Split the user input into words
            words = user_input.split()
            
            # Correct words that are not in the dictionary
            corrections_made = False  # Flag to check if any corrections were accepted
            for index, word in enumerate(words):
                # Check if the word is a number or contains digits; if yes, then continue to the next iteration
                if word.isdigit() or any(char.isdigit() for char in word):
                    continue
                
                # Check if word is a URL; if yes, continue to the next iteration
                if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', word):
                    continue

                # If the word is not in the dictionary
                if word not in spell:
                    # Get the most likely correct spelling for the word
                    suggestion = spell.correction(word)
                    
                    # If no suggestions are found, continue to the next iteration
                    if not suggestion:
                        continue
                    
                    # Display the suggestion to the user and ask for their choice
                    choice = input(f"Did you mean '{suggestion}' instead of '{word}'? (Y/n): ").lower()
                    
                    # If the user accepts the suggestion, replace the word in the list
                    if choice == 'y' or choice == '':
                        words[index] = suggestion
                        corrections_made = True  # Update the flag
            
            if corrections_made:  # Display the corrected input only if corrections were accepted
                corrected_input = ' '.join(words)
                print(f"\nYour corrected input is: {corrected_input}")
            else:
                corrected_input = user_input
            
            if user_input.lower() in ['quit', 'exit']:
                self.print_farewell_message()
                exit(0)
            
            return corrected_input







    def search_index(self, query_list: Union[list, str], indexdir: str, max_results: int = 10) -> list:
        """
        Search the index using the provided query list or a single query string and returns a list of matching lines.
        """
        try:
            ix = open_dir(indexdir)
        except Exception as e:
            logging.error(f"Error occurred while opening index directory: {e}")
            return []

        results_dict = {}
        searched_items = set()

        if isinstance(query_list, str):
            query_list = [{"services": [query_list]}]

        with ix.searcher() as searcher:
            for query in query_list:
                cves = query.get("cves", [])
                service_names = query.get("services", [])

                # Search for CVEs first if they exist
                for cve in cves:
                    if cve.lower() in searched_items:
                        continue

                    searched_items.add(cve.lower())
                    parsed_query = QueryParser("content", ix.schema).parse(cve.lower())
                    cve_results = []

                    try:
                        results = searcher.search(parsed_query, limit=max_results)
                        for res in results:
                            content = res['content']
                            lines = content.splitlines()
                            for line in lines:
                                prefix = line.split(":")[0].lower()
                                if cve.lower() in prefix:
                                    cve_results.append(line.strip())
                                    if len(cve_results) >= max_results:
                                        break

                        if cve_results:
                            results_dict[cve] = cve_results

                    except Exception as e:
                        logging.error(f"Error occurred while searching for CVE {cve}: {e}")

                # If services are specified, search for them
                for s in service_names:
                    if s.lower() in searched_items:
                        continue

                    searched_items.add(s.lower())
                    parsed_query = QueryParser("content", ix.schema).parse(s.lower())
                    service_results = []

                    try:
                        results = searcher.search(parsed_query, limit=max_results)
                        for res in results:
                            content = res['content']
                            lines = content.splitlines()
                            for line in lines:
                                prefix = line.split(":")[0].lower()
                                if s.lower() in prefix:
                                    service_results.append(line.strip())
                                    if len(service_results) >= max_results:
                                        break

                        if service_results:
                            results_dict[f"Service {s}"] = service_results

                    except Exception as e:
                        logging.error(f"Error occurred while searching for service {s}: {e}")

        formatted_results = []
        for key, values in results_dict.items():
            formatted_results.append(key + ":")
            formatted_results.extend(values)

        return formatted_results

        



    def parse_nmap(self, data):
        try:
            if not data or not isinstance(data, str):
                raise ValueError("The provided data is empty or not of type string.")

            hosts = re.split(r'Nmap scan report for ', data)
            if len(hosts) <= 1:
                raise ValueError("No valid Nmap reports found in the provided data.")

            parsed_results = []

            for host in hosts[1:]:  # Skip the first empty split
                match = re.search(r'([a-zA-Z0-9.-]+)?\s?(\([\d\.]+\))?', host)
                if not match:
                    continue

                device_name = match.group(1) or "Unknown"
                ip_address = match.group(2).replace("(", "").replace(")", "") if match.group(2) else "Unknown"

                ports = set()
                services = set()

                # Extract port, protocol, state, and service details
                service_matches = re.findall(r'(\d+)/(tcp|udp)\s+(\w+)\s+([\w-]+)', host)
                for match in service_matches:
                    port, _, state, service = match
                    if state == "open":
                        ports.add(port)
                        if service == "domain":  # Replace "domain" service with "dns"
                            services.add("dns")
                        else:
                            services.add(service)

                # Extract CVEs from host data
                cve_matches = re.findall(r'cve-\d{4}-\d+', host, re.IGNORECASE)  # Updated regex for CVE
                parsed_results.append({
                    "hostname": device_name,
                    "ip": ip_address,
                    "ports": list(ports),
                    "services": list(services),
                    "cves": cve_matches  # Add CVEs to the result
                })

            print("DONE")
            return parsed_results

        except Exception as e:
            print(f"Error occurred while parsing: {e}")
            return []




    def colored_output(self, text):
        """Color everything before the first ':' in red and the rest in yellow."""

        # Split the text at the first ':'
        parts = re.split('(:)', text, maxsplit=1)

        # Color everything before the first ':' in red
        if len(parts) > 1:
            colored_text = f'\033[91m{parts[0]}\033[0m\033[93m{parts[1]}{parts[2]}\033[0m'
        else:
            colored_text = f'\033[93m{text}\033[0m'

        return colored_text
    def get_input_with_validation(self, prompt: str, valid_fn: Optional[callable] = None) -> str:
        while True:
            user_input = input(colored(prompt, "cyan")).lower().strip()
            if valid_fn and not valid_fn(user_input):
                cprint("Invalid input. Please try again.", "red")
                continue
            return user_input

    def is_valid_command_choice(self, choice: str, max_choice: int) -> bool:
        if choice in ['back', 'b']:
            return True
        if choice.isdigit() and 0 < int(choice) <= max_choice:
            return True
        return False

    def is_valid_results_choice(self, choice: str) -> bool:
        return choice.isdigit() and int(choice) > 0



    def _process_previous_nmap_results(self) -> bool:
        """Internal method to process previous results and loop back to the main prompt."""
        self.display_command_list()

        try:
            cmd = self.get_input_with_validation(
                "Enter the number of the command you'd like to process results for (or type 'back' or 'b' to return): ",
                lambda x: self.is_valid_command_choice(x, len(self.command_history))
            )

            if cmd in ['back', 'b']:
                return True

            number_of_results = self.get_input_with_validation(
                "Enter the number of the processed results you would like to receive (or type 'back' or 'b' to return, 'all' or 'a' for all results): ",
                lambda x: x in ['back', 'b', 'all', 'a'] or self.is_valid_results_choice(x)
            )

            if number_of_results in ['back', 'b']:
                return True

            cmd_num = int(cmd)
            _, file_path = self.command_history[cmd_num - 1]
            with open(file_path, 'r') as f:
                result = f.read()
                services = self.parse_nmap(result)

                max_results_value = int(number_of_results) if number_of_results not in ['all', 'a'] else 1e6
                results = self.search_index(services, self.index_dir, max_results_value)

                if results:
                    idx = 1
                    for line in results:
                        if line.endswith(':'):
                            print(colored(line, 'yellow'))  # Service names will be displayed in yellow
                        else:
                            # Splitting based on the ':' and coloring the prefix in red
                            prefix, suffix = line.split(':', 1) if ':' in line else (line, '')
                            print(colored(f"{idx}. {prefix}:", 'red') + colored(f" {suffix}", 'blue'))
                            idx += 1

                    try:
                        selection = int(input(colored("\nSelect a result number to modify or any other key to continue: ", 'blue')))
                        if 1 <= selection < idx:  # Since idx has been incremented in the loop
                            content_after_colon = results[selection - 1].split(':', 1)[1].strip() if ':' in results[selection - 1] else results[selection - 1]

                            readline.set_startup_hook(lambda: readline.insert_text(content_after_colon))
                            try:
                                modified_content = input(colored("\nEnter the modified content (or press enter to keep it unchanged): ", 'blue'))
                            finally:
                                readline.set_startup_hook()

                            if modified_content:
                                content_after_colon = modified_content

                            self.run_command(content_after_colon)
                            return True
                        else:
                            print("Invalid selection!")
                    except ValueError:
                        pass
                else:
                    print("No results found.")
                    return True
        except ValueError as ve:
            cprint(str(ve), "red")
        except Exception as e:
            cprint(f"An unexpected error occurred: {e}", "red")
        return True




    def _view_previous_results(self) -> bool:
        """Internal method to display previous results and loop back to the main prompt."""
        
        # Check if there are no previous results
        if not self.command_history:
            cprint("No previous results available.", "red")
            return True  # Return to the main loop
        
        self.display_command_list()
        
        try:
            cmd = input(colored("Enter the number of the command you'd like to view results for (or type 'back' or 'b' to return): ", "cyan"))
            if re.findall(r'(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z\d]+', cmd):
                raise ValueError
            if cmd.lower().strip() == 'back' or cmd.lower().strip() == 'b':
                return True  # Indicate that the user wants to return to the main loop
            
            if cmd.lower().strip() != 'back' and cmd.lower().strip() !='b':
                cmd_num = int(cmd)
                if 0 < cmd_num <= len(self.command_history):
                    _, file_path = self.command_history[cmd_num - 1]
                    with open(file_path, 'r') as f:
                        result = f.read()
                    cprint(f"\nResults for command #{cmd_num}:", "cyan")
                    cprint(result, "magenta")
                else:
                    cprint(f"Invalid number. Please choose between 1 and {len(self.command_history)}.", "red")
        except ValueError:
            cprint("Please enter a valid number or type 'back'.", "red")
        return True  # Indicate the user is still in the results view mode



    def generate_and_display_text(self, prompt: str) -> str:
        """Generate and display text based on a given prompt.

        Args:
            prompt (str): The input prompt for text generation.

        Returns:
            str: The cleaned-up generated text.
        """
        try:
            generated_text = self.generate_text(prompt)
            prompt_ip = self._extract_ip(prompt)
            urls = self.extract_urls(prompt)
            first_clean_up = self.ensure_space_between_letter_and_number(generated_text)
            second_clean_up = self.process_string(first_clean_up, prompt_ip, urls)
            try:
                help = self.extract_and_match_flags(second_clean_up)
                if help:
                    cprint("Verify that the flags used in the command matches your intent:", "magenta")
                    for h in help:
                        cprint("\n" + h, "red")
            except:
                logging.error("unable to extract")

            
            cprint("\nGenerated Command:", "cyan")
            cprint(second_clean_up, "magenta")
            cprint("-" * 50, "blue")
            
            return second_clean_up
        except Exception as e:
            logging.error(f"Error during text generation and display: {e}")
            cprint("An unexpected error occurred during text generation and display. Please try again or check logs.", "red")
            # Depending on your application's need, you might want to return an empty string or the original prompt.
            return prompt  # This returns the original prompt as a fallback. Adjust as needed.
            
    def run_command(self, text: str) -> None:
        """
        A function to run a command in the background based on the generated text.
        """
        def threaded_function():
            self.run_command_and_alert(text)
            self.command_running = False  # Set the flag to False once the command is done executing.

        # Before starting the thread, set the command_running flag to True.
        self.command_running = True
        thread = threading.Thread(target=threaded_function)
        thread.start()

        # Inform user that command has started
        print("\nThe operation has been initiated.")

      
        return self.get_user_prompt()




    def user_search_interface(self):
        """Provide a user interface for searching."""
        while True:
            query_str = input(colored("\nEnter your query, use keywords such as protocols HTTP, SSH, SMB or port numbers 443, 80 etc (or 'q' to quit): ", 'blue'))
            if query_str.lower() == "q":
                break

            # Ask the user for the number of results or 'all'
            num_results = input(colored("\nHow many results would you like? (Enter a number, 'all', or press enter for default): ", 'blue'))
            if num_results.lower() == "all":
                results = self.search_index(query_str, self.index_dir, max_results=float('inf'))  # Using float('inf') to symbolize "all"
            elif num_results == "":
                results = self.search_index(query_str,self.index_dir)  # Default
            else:
                try:
                    num = int(num_results)
                    results = self.search_index(query_str,self.index_dir, max_results=num)
                except ValueError:
                    print(colored("Invalid input. Using default number of results.", 'red'))
                    results = self.search_index(query_str,self.index_dir)  # Default

            # Shuffle the results
            random.shuffle(results)

            if results:
                for idx, line in enumerate(results, 1):
                    colored_line = self.colored_output(line)  # Assuming colored_output is a method of the class
                    print(f"{idx}. {colored_line}")

                try:
                    selection = int(input(colored("\nSelect a result number to modify or any other key to continue: ", 'blue')))
                    if 1 <= selection <= len(results):
                        content_after_colon = results[selection - 1].split(':', 1)[1].strip() if ':' in results[selection - 1] else results[selection - 1]
                        
                        # Using readline to set the default value for input
                        readline.set_startup_hook(lambda: readline.insert_text(content_after_colon))
                        try:
                            modified_content = input(colored("\nEnter the modified content (or press enter to keep it unchanged): ", 'blue'))
                        finally:
                            readline.set_startup_hook()  # Unset the hook after the input is done

                        # If user entered some modification, use it, otherwise stick with the original content
                        if modified_content:
                            content_after_colon = modified_content

                        self.run_command(content_after_colon)
                        return
                    else:
                        print("Invalid selection!")
                except ValueError:
                    # User did not enter a valid number, continue without error
                    pass
            else:
                print("No results found.")
                return



    def notify_command_status(self):
        """
        Notify user about command status.
        """
        if self.command_running:
            print("\nThe operation has been initiated. You'll be notified once it's complete.")
        else:
            print("\nCommand completed!")
            with self.print_lock:
                self.get_user_prompt()

    def get_modified_command(self, text: str) -> str:
        """Prompt the user to modify and return a command.

        Args:
            text (str): The proposed command.

        Returns:
            str: The modified command.
        """
        try:
            # Use the readline library to pre-fill the input field with the given text
            readline.set_startup_hook(lambda: readline.insert_text(text))

            cprint("\nThe current command is:", "cyan", end=" ")
            cprint(text, "magenta")

            # Prompt the user to modify the command
            modified_text = input("\nModify the command as needed and press Enter: ")

            # Reset the readline startup hook
            readline.set_startup_hook()

            return modified_text

        except Exception as e:
            logging.error(f"Error during modified command prompt: {e}")
            cprint("An unexpected error occurred while modifying the command. Please try again or check logs.", "red")
            return text  # Return the original text as a fallback


    def handle_generated_text(self, text):
        """Handle the generated text based on user's choice or predefined actions.

        Args:
            text (str): The generated text or command.
        """
        try:
            # If always_apply_action is set, simply run the command
            if self.always_apply_action:
                self.run_command(text)
                return
            
            # Ask the user for their action choice
            action_choice = self.get_action_choice()

            # If 'always' is chosen, set the flag and run the command
            if action_choice in ['always', 'a']:
                self.always_apply_action = True
                self.run_command(text)
            # If 'yes' is chosen, let the user modify the command and then run it
            elif action_choice in ['yes', 'y']:
                modified_command = self.get_modified_command(text)
                self.run_command(modified_command if modified_command else text)
        except Exception as e:
            logging.error(f"Error handling generated text: {e}")
            cprint("An error occurred while handling the generated text. Please try again or check logs.", "red")


    def get_action_choice(self) -> str:
        """Prompt user to make a choice on the action to take with the generated text.

        Returns:
            str: The action choice made by the user.
        """
        action_choice_prompt = colored("Do you want to run a command based on the generated text?", "yellow")
        options = colored("(y/n/a) (yes/no/always):", "green")
        
        while True:  # Loop until a valid choice is made
            try:
                action_choice = input(action_choice_prompt + " " + options).lower().strip()
                if action_choice in ['yes', 'y', 'no', 'n', 'always', 'a']:
                    return action_choice
                else:
                    cprint("Invalid choice. Please enter 'y', 'n', or 'a'.", "red")
                    # Reset with a new line to avoid the previous message appearing highlighted
                    print("")
            except Exception as e:
                logging.error(f"Error during action choice prompt: {e}")
                cprint("An unexpected error occurred during action choice. Please try again or check logs.", "red")


def main_func():
    generator = InteractiveGenerator()
    generator.start_interactive_mode()

if __name__ == "__main__":
    main_func()