# src/algorithms/base.py
# Base classes for evolutionary algorithms

from abc import ABC, abstractmethod
import random
import numpy as np

class Individual(ABC):
    """
    Abstract base class for an individual in an evolutionary algorithm.
    
    An individual represents a potential solution to the problem being solved.
    """
    def __init__(self, value=None, init_params=None):
        if value is not None:
            self.value = value
        else:
            self.value = self._random_init(init_params)

    @abstractmethod
    def pair(self, other, pair_params):
        """
        Create a new individual by combining this individual with another.
        
        Args:
            other: Another individual to pair with
            pair_params: Dictionary of parameters for pairing
            
        Returns:
            A new individual resulting from the pairing
        """
        pass

    @abstractmethod
    def mutate(self, mutate_params):
        """
        Mutate this individual to introduce variation.
        
        Args:
            mutate_params: Dictionary of parameters for mutation
            
        Returns:
            Boolean indicating whether mutation occurred
        """
        pass

    @abstractmethod
    def _random_init(self, init_params):
        """
        Initialize this individual with random values.
        
        Args:
            init_params: Dictionary of parameters for initialization
            
        Returns:
            Initial value for this individual
        """
        pass


class Population:
    """
    A population of individuals in an evolutionary algorithm.
    """
    def __init__(self, size, fitness, individual_class, init_params):
        """
        Initialize a population of individuals.
        
        Args:
            size: Number of individuals in the population
            fitness: Function to evaluate fitness of individuals
            individual_class: Class to create individuals
            init_params: Parameters for initializing individuals
        """
        self.fitness = fitness
        self.individuals = [individual_class(init_params=init_params) for _ in range(size)]
        self.individuals.sort(key=lambda x: self.fitness(x))

    def replace(self, new_individuals):
        """
        Replace worst individuals with new ones, maintaining population size.
        
        Args:
            new_individuals: List of new individuals to add to population
        """
        size = len(self.individuals)
        self.individuals.extend(new_individuals)
        self.individuals.sort(key=lambda x: self.fitness(x))
        self.individuals = self.individuals[-size:]  # Keep only the best individuals

    def get_best_individual(self):
        """Return the individual with the highest fitness"""
        return self.individuals[-1]
        
    def tournament_selection(self, tournament_size):
        """
        Select one individual via tournament selection.
        
        Args:
            tournament_size: Number of individuals competing in each tournament
            
        Returns:
            The winning individual from the tournament
        """
        contestants_indices = random.sample(range(len(self.individuals)), tournament_size)
        best_idx = contestants_indices[0]
        
        for idx in contestants_indices[1:]:
            if self.fitness(self.individuals[idx]) > self.fitness(self.individuals[best_idx]):
                best_idx = idx
                
        return self.individuals[best_idx]


class Evolution:
    """
    Core evolutionary algorithm implementation.
    """
    def __init__(self, pool_size, fitness, individual_class, n_offsprings, 
                 pair_params, mutate_params, init_params, tournament_size=5):
        """
        Initialize the evolutionary algorithm.
        
        Args:
            pool_size: Size of the population
            fitness: Function to evaluate individual fitness
            individual_class: Class to create individuals
            n_offsprings: Number of offspring to create per generation
            pair_params: Parameters for pairing individuals
            mutate_params: Parameters for mutating individuals
            init_params: Parameters for initializing individuals
            tournament_size: Size of tournaments for selection
        """
        self.pair_params = pair_params
        self.mutate_params = mutate_params
        self.pool = Population(pool_size, fitness, individual_class, init_params)
        self.n_offsprings = n_offsprings
        self.tournament_size = tournament_size

    def step(self):
        """
        Take one evolution step (one generation).
        
        Returns:
            Number of mutations that occurred
        """
        new_individuals = []
        mutation_count = 0
        
        # Elitism: always keep best individual
        new_individuals.append(self.pool.get_best_individual())
        
        # Create remaining individuals through tournament selection, crossover, and mutation
        while len(new_individuals) < len(self.pool.individuals):
            # Tournament selection for parents
            parent1 = self.pool.tournament_selection(self.tournament_size)
            parent2 = self.pool.tournament_selection(self.tournament_size)
            
            # Create offspring through crossover
            offspring = parent1.pair(parent2, self.pair_params)
            
            # Mutate offspring and track if mutation occurred
            if offspring.mutate(self.mutate_params):
                mutation_count += 1
                
            new_individuals.append(offspring)
            
        # Replace population with new individuals
        self.pool.individuals = new_individuals
        
        return mutation_count