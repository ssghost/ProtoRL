from protorl.agents.base import Agent


class DuelingDQNAgent(Agent):
    def __init__(self, actor, learner,
                 replace=1000, update_actor=1):
        super().__init__(actor=actor, learner=learner)
        self.replace_target_cnt = replace
        self.learn_step_counter = 0
        self.update_actor = update_actor

    def choose_action(self, observation):
        action = self.actor.choose_action(observation)
        return action

    def update_networks(self):
        if self.learn_step_counter % self.replace_target_cnt == 0:
            src = self.learner.q_eval
            dest = self.learner.q_next
            self.learner.update_network_parameters(src, dest, tau=1.0)

        if self.learn_step_counter % self.update_actor == 0:
            src = self.learner.q_eval
            dest = self.actor.q_eval
            self.actor.update_network_parameters(src, dest, tau=1.0)

    def update(self, transitions):
        self.learner.update(transitions)
        self.learn_step_counter += 1
        self.update_networks()
