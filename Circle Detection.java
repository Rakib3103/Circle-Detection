import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.highgui.HighGui;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

public class CircleDetector {
    private String image_path;
    private int population_size;
    private int max_generations;
    private Mat img;
    private int height, width;
    private List<int[]> population;
    private double best_fitness = Double.POSITIVE_INFINITY;
    private int[] best_individual = null;
    private List<Double> fitness_values = new ArrayList<Double>();

    public CircleDetector(String image_path, int population_size, int max_generations) {
        this.image_path = image_path;
        this.population_size = population_size;
        this.max_generations = max_generations;
        this.img = Imgcodecs.imread(this.image_path, Imgcodecs.IMREAD_GRAYSCALE);
        this.height = this.img.height();
        this.width = this.img.width();
        this.population = new ArrayList<int[]>();
    }

    public void initialize_population() {
        Random rand = new Random();
        for (int i = 0; i < this.population_size; i++) {
            int[] individual = new int[3];
            int x = rand.nextInt(this.width);
            int y = rand.nextInt(this.height);
            int r = rand.nextInt(Math.min(this.width, this.height)/2) + 1;
            individual[0] = x;
            individual[1] = y;
            individual[2] = r;
            this.population.add(individual);
        }
    }

    public double evaluate_fitness(int[] individual) {
        double fitness = 0;
        for (int i = 0; i < this.width; i++) {
            for (int j = 0; j < this.height; j++) {
                int x = individual[0];
                int y = individual[1];
                int r = individual[2];
                double distance = Math.sqrt(Math.pow(i - x, 2) + Math.pow(j - y, 2));
                fitness += Math.abs(distance - r - this.img.get(j, i)[0]);
            }
        }
        return fitness;
    }

    public List<int[]> selection() {
        double fitness_sum = 0;
        for (Double fitness : this.fitness_values) {
            fitness_sum += fitness;
        }
        List<Double> probabilities = new ArrayList<Double>();
        for (Double fitness : this.fitness_values) {
            probabilities.add(fitness/fitness_sum);
        }
        List<Integer> selected_indices = new ArrayList<Integer>();
        while (selected_indices.size() < this.population_size/2) {
            double rand = Math.random();
            double cumulative_probability = 0;
            for (int i = 0; i < probabilities.size(); i++) {
                cumulative_probability += probabilities.get(i);
                if (rand <= cumulative_probability) {
                    selected_indices.add(i);
                    break;
                }
            }
        }
        List<int[]> selected_individuals = new ArrayList<int[]>();
        for (int i = 0; i < selected_indices.size(); i++) {
            selected_individuals.add(this.population.get(selected_indices.get(i)));
        }
        return selected_individuals;
    }

    public int[][] crossover(int[] parent1, int[] parent2) {
        int[][] children = new int[2][3];
        Random rand = new Random();
        int crossover_point = rand.nextInt(3);
        for (int i = 0;
