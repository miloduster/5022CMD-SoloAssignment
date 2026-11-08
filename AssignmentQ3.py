"""Q3: Fibonacci(35), Fibonacci(38), Fibonacci(40)
Compares execution time WITH and WITHOUT multithreading"""

import threading #allows program to create multiple threads to perform tasks
import time #import python time module, use it to measure

NUMBERS = [35, 38, 40] #list containing three Fibonacci inputs
ROUNDS = 10 #tells the program to repeat experiment 10 times

def fibonacci(n):
    """Return the nth Fibonacci number using recursion."""
    if n <= 1:  #base case, 0,1 are starting points so is used as stopping condition
        return n
    return fibonacci(n-1) + fibonacci(n-2)  #recursive

#n = which fibonacci num this thread must calculate
#results = shared array where final answers are stored
#index = which position in the array this thread should use (entire array is passed into this method)
def worker(n, results, index):
    """Thread task: calculate fib(n) and store it in its own slot"""
    results[index] = fibonacci(n) #stores the final answer

def with_threads():
    """One thread per number. Returns (results, T in ns)."""
    #len(NUMBERS) counts how many items are in the NUMBERS list
    #makes three empty slots in the result array.
    results = [None] * len(NUMBERS)

    #threading.Thread creates a new thread
    #target = worker tells to execute the worker() function.
    #enumerate = return you an index and number
    #n is number values
    threads = [threading.Thread(target=worker, args=(n, results, i)) for i, n
                in enumerate(NUMBERS)]

    #records the starting
    t1 = time.perf_counter_ns() #just before the first thread starts
    #start all threads
    for t in threads:
        t.start() #the loop does threads[0].start()
    for t in threads:
        t.join() #tells main program to wait for threads to finish before continuing
    t2 = time.perf_counter_ns()
    return results, t2 - t1

def without_threads():
    """Creates a function that calculates same three fibo numbers without thread creation."""
    t1 = time.perf_counter_ns()
    results = [fibonacci(n) for n in NUMBERS] #calculate fibo numbers and append them in a list
    t2 = time.perf_counter_ns()
    return results, t2 - t1 #the three completed answers, and the total time taken by multithreaded calculation


def run_experiment(title, task):
    """Run the task for ROUNDS(10) rounds, print each T, return the average T."""
    print(f"\n=== Fibonacci Computation ({title}) ===")
    total = 0 #used to add up the time taken across all 10 rounds.
    for r in range(1, ROUNDS + 1): #repeat the experiment 10 times
        results, t = task() #executes the selected task
        total += t

        # prepares the fib answers so can be printed neatly
        # #zip() pairs the OG numbers with the results
        #n represents the OG Fibonacci input
        #v represents the calculated answer
        #join() combines all three pieces of text with commas between them
        values = ", ".join(f"Fib({n})={v}" for n, v in zip(NUMBERS, results))

        #prints the round number, Fibonacci answers and time taken
        #{r:>2}	Aligns the round number to the right using two character spaces.
        #{values}	Displays the Fibonacci answers.
        #{t:,}	Displays the time with commas for easier reading.
        #ns	Indicates nanoseconds.
        print(f"Round {r:>2}: {values} | T = {t:,} ns")

    # The // operator means integer division. It divides and rounds down to a whole number.
    average = total // ROUNDS
    #displays the average time for the experiment
    print(f"Average T ({title}): {average:,} ns")
    return average #sends the average back


threaded = run_experiment("With Multithreading", with_threads)
sequential = run_experiment("Without Multithreading", without_threads)

#compares the two average times
#calculates the percentage change in execution time
change = (sequential - threaded) / sequential * 100

#prints a sentence describing the comparison.
#abs() returns the absolute value, which removes the negative sign.
#if else statement prints reduced if is zero/positive, increased otherwise.
print(f"\nObservation: multithreading {'reduced' if change >= 0 else 'increased'} "
      f"the average time by {abs(change):.1f}%.")