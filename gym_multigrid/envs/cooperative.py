from gym_multigrid.multigrid import *

class Cooperative(MultiGridEnv):
    """
    Environment in which the agents have to get food/rewards from exploiting predator prey dynamics

    Grid size = 20
    Num agents = 4
    Time per Episode = 90
    Agents view size = (3 x 3)

    """

    def __init__(
        self,
        size=25,
        width=None,
        height=None,
        num_balls=[],
        agents_index = [],
        balls_index=[],
        balls_reward=[],
        zero_sum = False,
        view_size=3

    ):
        self.num_balls = num_balls
        self.balls_index = balls_index
        self.balls_reward = balls_reward
        self.zero_sum = zero_sum

        self.world = World

        agents = []
        for i in agents_index:
            agents.append(Agent(self.world, i, view_size=view_size, rect_view=False))

        super().__init__(
            grid_size=size,
            width=width,
            height=height,
            max_steps= 10000,
            # Set this to True for maximum speed
            see_through_walls=False,
            agents=agents,
            agent_view_size=view_size
        )



    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(self.world, 0, 0)
        self.grid.horz_wall(self.world, 0, height-1)
        self.grid.vert_wall(self.world, 0, 0)
        self.grid.vert_wall(self.world, width-1, 0)

        for number, index, reward in zip(self.num_balls, self.balls_index, self.balls_reward):
            for i in range(number):
                self.place_obj(Ball(self.world, index, reward))

        # Randomize the player start position and orientation
        for a in self.agents:
           self.place_agent(a)

        # For debugging purposes; the things I do for a rectangular grid :(
        #agents_loc = [(10, 10), (10, 20), (20, 10), (20, 20)]
        #for i, a in enumerate(self.agents):
            #self.put_obj(a, agents_loc[i][0], agents_loc[i][1])


        self.put_obj(Ball(self.world, index, reward), 0, 0)


    def _reward(self, i, rewards, reward=1):
        """
        Compute the reward to be given upon success
        """
        for j,a in enumerate(self.agents):
            if a.index==i or a.index==0:
                rewards[j]+=reward
            if self.zero_sum:
                if a.index!=i or a.index==0:
                    rewards[j] -= reward

    def _handle_pickup(self, i, rewards, fwd_pos, fwd_cell):
        if fwd_cell:
            if fwd_cell.can_pickup():
                if fwd_cell.index in [0, self.agents[i].index]:
                    fwd_cell.cur_pos = np.array([-1, -1])
                    self.grid.set(*fwd_pos, None)
                    self._reward(i, rewards, fwd_cell.reward)

    def _handle_drop(self, i, rewards, fwd_pos, fwd_cell):
        pass

    def step(self, actions):
        obs, rewards, done, info = MultiGridEnv.step(self, actions)
        return obs, rewards, done, info


class Cooperative4HEnv(Cooperative):
    def __init__(self):
        super().__init__(size=25,
        num_balls=[5],
        agents_index = [1,2,3,4],
        balls_index=[0],
        balls_reward=[1],
        zero_sum=True)

