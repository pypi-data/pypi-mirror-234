def eval(
    policy, env_name, state_scaler, env_config={}, device="cpu", epochs=20, render=False
):
    policy.eval()
    policy.to(device)
    if env_config:
        env = gym.make(env_name, config=env_config)
    else:
        env = gym.make(env_name)
    env.seed(SEED)
    action_min = env.action_space.low[0]
    action_max = env.action_space.high[0]
    episode_rewards = []
    actions = []
    for epoch in range(epochs):
        state, info = env.reset()
        if isinstance(state, dict):
            state = state["obs"]
        scaled_state = state_scaler.scale_state(state)
        done = False
        total_reward = 0
        steps = 0
        while not done:
            with torch.no_grad():
                action, _ = select_action(
                    policy, scaled_state, device, action_min, action_max
                )
            action = action.numpy()
            actions.append(action)
            next_state, reward, done, truncated, info = env.step(action)
            done = done or truncated
            if isinstance(next_state, dict):
                next_state = next_state["obs"]
            scaled_next_state = state_scaler.scale_state(next_state)
            if render:
                env.render()
            scaled_state = scaled_next_state
            total_reward += reward
            steps += 1
        else:
            episode_rewards.append(total_reward)
    policy.train()
    return episode_rewards, actions
