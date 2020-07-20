import random


class NaiveGeneticAlgorithm:
    def __init__(self, size, dimension, sol_range, chrom_size, cp, mp, gen_max, fitness_function, fitness_symbol):
        # 种群信息
        self.individuals = []  # 个体信息
        self.fitness = []  # 适应度
        self.select_pro = []  # 选择概率
        self.new_individuals = []  # 新一代个体
        self.dimension = dimension  # 变量维度
        self.sol_range = sol_range
        self.interval = sol_range[1] - sol_range[0]  # 求解范围
        self.elitist = {'chromosome': [0 for _ in range(self.dimension)], 'fitness': float('-inf')}

        # 超参数
        self.size = size  # 种群规模
        self.chrom_size = chrom_size  # 染色体长度
        self.cross_over = cp  # 交叉变异概率
        self.mutation = mp  # 突变概率
        self.generation_max = gen_max
        self.fitness_symbol = fitness_symbol  # 判断函数的fitness全是正，全是负，还是有正有负

        # 初始化种群
        binary_length = 2 ** self.chrom_size - 1  # 二进制长度
        for i in range(self.size):
            self.individuals.append([random.randint(0, binary_length) for _ in range(self.dimension)])
            self.new_individuals.append([0 for _ in range(self.dimension)])
            self.fitness.append(float('-inf'))
            self.select_pro.append(0.0)

        # 评价函数
        self.fitness_function = fitness_function

    def decode(self, chromosome):   # 解码后的十进制数
        binary_num = 2 ** self.chrom_size - 1
        decode_num = self.sol_range[0] + chromosome * self.interval / binary_num

        return decode_num

    def fitness_sol(self, chroms):
        variables = [self.decode(chrom) for chrom in chroms]
        res = self.fitness_function(variables)

        return res

    def evaluate(self):  # 进行打分
        sp = self.select_pro
        for i in range(self.size):
            # 对正负fitness的结果进行调整
            if self.fitness_symbol == '+':
                self.fitness[i] = self.fitness_sol(self.individuals[i])
            elif self.fitness_symbol == '-':
                self.fitness[i] = 1 / self.fitness_sol(self.individuals[i])
            else:
                self.fitness[i] = self.fitness_sol(self.individuals[i]) if self.fitness_sol(self.individuals[i]) >= 0 \
                    else 0
        fitness_sum = sum(self.fitness)
        for i in range(self.size):
            sp[i] = self.fitness[i] / float(fitness_sum)
        for i in range(1, self.size):
            sp[i] = sp[i] + sp[i-1]  # 概率累加为1

    def select(self):  # 选择染色体
        t = random.random()
        i = 0
        for p in self.select_pro:
            if p > t:
                break
            i += 1

        return i

    def cross(self, chrom1, chrom2):
        p = random.random()
        binary_length = 2 ** self.chrom_size - 1
        if chrom1 != chrom2 and p < self.cross_over:  # 进行交叉变异
            cross_point = random.randint(1, self.chrom_size-1)  # 交叉点
            mask = binary_length << cross_point
            r1, r2 = chrom1 & mask, chrom2 & mask
            mask = binary_length >> (self.chrom_size - cross_point)
            l1, l2 = chrom1 & mask, chrom2 & mask
            chrom1, chrom2 = r1 + l2, r2 + l1

        return [chrom1, chrom2]

    def mutate(self, chrom):
        p = random.random()
        if p < self.mutation:
            mutate_point = random.randint(1, self.chrom_size)
            mask1 = 1 << (mutate_point - 1)
            mask2 = chrom & mask1
            if mask2 > 0:
                chrom = chrom & (~mask2)
            else:
                chrom = chrom ^ mask1

        return chrom

    def save_elitist(self):
        j = -1
        for i in range(self.size):
            if self.elitist['fitness'] < self.fitness[i]:
                j = i
                self.elitist['fitness'] = self.fitness[i]

        if j >= 0:
            for i in range(self.dimension):
                self.elitist['chromosome'][i] = self.individuals[j][i]

    def evolve(self):
        self.evaluate()
        i = 0
        while True:
            individual1 = self.select()
            individual2 = self.select()
            ind1_set = [None] * self.dimension
            ind2_set = [None] * self.dimension

            # 交叉
            for dim in range(self.dimension):
                ind1_set[dim] = self.individuals[individual1][dim]
                ind2_set[dim] = self.individuals[individual2][dim]

                [ind1_set[dim], ind2_set[dim]] = self.cross(ind1_set[dim], ind2_set[dim])

                # 变异
                ind1_set[dim] = self.mutate(ind1_set[dim])
                ind2_set[dim] = self.mutate(ind2_set[dim])

                self.new_individuals[i][dim] = ind1_set[dim]
                self.new_individuals[i+1][dim] = ind2_set[dim]

            i += 2
            if i >= self.size:
                break

        self.save_elitist()

        for i in range(self.size):
            for j in range(self.dimension):
                self.individuals[i][j] = self.new_individuals[i][j]

    def solver(self):
        for i in range(self.generation_max):
            self.evolve()
            best_sol = []
            print("Epoch {}, maximum fitness is {}, mean fitness is {}".format(i, max(self.fitness), sum(self.fitness) / self.size))
            best_index = self.fitness.index(max(self.fitness))
            for j in self.individuals[best_index]:
                best_sol.append(self.decode(j))
            print("Best solution is {}".format(best_sol))

