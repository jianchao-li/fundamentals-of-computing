"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = float(0)
        self._current_cookies = float(0)
        self._current_time = float(0)
        self._current_cps = float(1)
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        info_str = ""
        info_str += ("Total cookies: " + str(self._total_cookies))
        info_str += (", Current cookies: " + str(self._current_cookies))
        info_str += (", Time: " + str(self._current_time))
        info_str += (", CPS: " + str(self._current_cps))
        return info_str
            
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.get_cookies() >= cookies:
            return float(0)
        else:
            return float(math.ceil((cookies - self.get_cookies()) / self._current_cps))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
            self._current_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.get_cookies() >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))
            # provided.update_item(item_name)
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy. Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    clicker = ClickerState()
    build_info_cp = build_info.clone()
    while True:
        if clicker.get_time() > duration:
            break
        item_to_buy = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(), build_info_cp)
        if item_to_buy:
            item_cost = build_info_cp.get_cost(item_to_buy)
            time_to_wait = clicker.time_until(item_cost)
            if clicker.get_time() + time_to_wait > duration:
                clicker.wait(duration - clicker.get_time())
                break
            else:
                clicker.wait(time_to_wait)
                item_cps = build_info_cp.get_cps(item_to_buy)
                clicker.buy_item(item_to_buy, item_cost, item_cps)
                build_info_cp.update_item(item_to_buy)
        else:
            clicker.wait(duration - clicker.get_time())
            break
    return clicker
        
def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left. Your
    simulate_clicker function must be able to deal with such broken
    strategies. Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    afford_cost = cps * time_left + cookies
    items = build_info.build_items()
    cheap_item = None
    cheap_cost = float('inf')
    for item in items:
        cost = build_info.get_cost(item)
        if cost <= afford_cost and cost < cheap_cost:
            cheap_item = item
            cheap_cost = cost
    return cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    afford_cost = cps * time_left + cookies
    items = build_info.build_items()
    expensive_item = None
    expensive_cost = float('-inf')
    for item in items:
        cost = build_info.get_cost(item)
        if cost <= afford_cost and cost > expensive_cost:
            expensive_item = item
            expensive_cost = cost
    return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    afford_cost = cps * time_left + cookies
    items = build_info.build_items()
    quick_item = None
    quick_rate = float('-inf')
    for item in items:
        cost = build_info.get_cost(item)
        rate = build_info.get_cps(item) / build_info.get_cost(item)
        if cost <= afford_cost and rate > quick_rate:
            quick_item = item
            quick_rate = rate
    return quick_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

