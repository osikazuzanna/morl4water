import numpy as np
import mo_gymnasium
import examples.omo_river_simulation


#TODO make envs for omo
water_management_system = mo_gymnasium.make('omo-v0')


def run_omo():

    #reset
    obs, info = water_management_system.reset()
    print(f'Initial Obs: {obs}')

    final_truncated = False
    final_terminated = False
    for t in range(248):
        if not final_terminated and not final_truncated:
            action = water_management_system.action_space.sample()
            # # print("AAAAACTION ", action)
            # action = np.array([0.3,0.23,0.1]) #ADDED FOR COMPARISON [0.8,0.5,0.1], [0.3,0.23,0.1]
            print(f'Action for month: {t}: {action}')

            (
                        final_observation,
                        final_reward,
                        final_terminated,
                        final_truncated,
                        final_info
                    ) = water_management_system.step(action)
            # print(f'Final final_info: ', final_info)
            print(f'Observation: {final_observation}')
            print(f'Reward: {final_reward}')
            
        else:
            break

    return final_observation


run_omo()