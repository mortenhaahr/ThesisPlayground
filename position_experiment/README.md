# Overview of repo
Files:
- `position_experiment.py`: Source code for the experiment. Based of https://dl.acm.org/doi/pdf/10.1145/3567591
- `requirements.txt`: Python dependencies

Figures:
- `autodiff_model_-_with_tau.png`: AD-direct solution with time transformation.
- `autodiff_model.png`: AD-direct solution without time transformation.
- `pinn_model_-_with_tau.png`: Physics-Informed Neural Network (PINN) solution with time transformation.
- `pinn_model_(if_lucky).png`: PINN solution without time transformation - sometimes we get lucky and get somewhat sensible results.
- `pinn_model_at_low_time_period.png`: PINN solution without time transformation but where the scale of time is decreased by a factor 100.
- `pinn_model.png`: PINN solution without time transformation - most of the time results are terrible.
- `vanilla_model_-_with_tau.png`: Vanilla model solution with time transformation.
- `vanilla_model.png`: Vanilla model solution without time transformation.