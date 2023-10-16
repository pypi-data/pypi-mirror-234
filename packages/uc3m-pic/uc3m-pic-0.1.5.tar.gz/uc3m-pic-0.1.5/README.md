# UC3M-PIC

Computer Vision class evaluation module for Master in Robotics and Automation at UC3M

## Login

Before evaluating your models, login with GCP credentials:

```
import uc3m_pic
student = uc3m_pic.eval.User(user_id)
student.login(os.path.join(path_to_credentials))
student.open_by_url(url)
```

## Evaluation

Submit your model for evaluation and leaderboard update:

```
student.submit(best_model, exercise=exercise_number)
```