import os
import gspread
import uc3m_pic
import torch
import torchvision
import torchmetrics
import json
import hashlib

from sklearn.model_selection import StratifiedShuffleSplit
from google.auth import default
from google_auth_oauthlib.flow import InstalledAppFlow
from tqdm.auto import tqdm


# Search for string in worksheet and return column and row
def find_cell(worksheet, string):
    for cell in worksheet.findall(string):
        if cell.value == string:
            return cell.col, cell.row
    return None


class User():
    def __init__(self, user_id: str = '100100100'):
        self.user_id = user_id
    
    # def login(self):
    #     try:
    #         self.creds, _ = default(scopes=['https://www.googleapis.com/auth/spreadsheets'])
    #         self.gs = gspread.authorize(self.creds)
    #     except Exception as e:
    #         print(e)

    def login(self, json_path: str = 'creds.json'):
        try:
            from google.colab import auth
            auth.authenticate_user()

            self.creds, _ = default()
            self.gs = gspread.authorize(self.creds)
        except:
            self.gs = gspread.oauth(credentials_filename=json_path, 
                scopes=['https://www.googleapis.com/auth/spreadsheets'])

    def login_remote(self, json_path: str = 'creds.json', port: int = 8157):
        flow = InstalledAppFlow.from_client_config(
            client_config=json.load(open(json_path)),
            scopes=["https://www.googleapis.com/auth/spreadsheets"])

        self.creds = flow.run_local_server(
            host="localhost",
            port=port,
            authorization_prompt_message="Please visit this URL: {url}",
            success_message="The auth flow is complete; you may close this window.",
        )

        self.gs = gspread.authorize(self.creds)

    def open_by_url(self, url: str):
        self.spreadsheet = self.gs.open_by_url(url)
        self.leaderboard = self.spreadsheet.worksheet('Leaderboard')
        ids = self.leaderboard.col_values(4)
        self.__row = ids.index(self.user_id)+1 if self.user_id in ids else -1
        if self.__row == -1:
            raise Exception('User not found in leaderboard. Please, initialize User with a valid user_id')
    
    def submit(self, model, exercise: int = 0):
        if exercise == 0:
            score = eval_model(model, torch.nn.MSELoss(reduction='sum'), exercise)
        elif exercise == 1:
            score = eval_model(
                model, torch.nn.CrossEntropyLoss(reduction='sum'), exercise, 
                metrics_fn=torchmetrics.classification.MulticlassAccuracy(
                    num_classes=10, average='micro'))
        elif exercise == 2:
            score = eval_model(
                model, torch.nn.CrossEntropyLoss(reduction='sum'), exercise, 
                metrics_fn=torchmetrics.classification.MulticlassAccuracy(
                    num_classes=47, average='micro'))
        elif exercise == 3:
            score = eval_model(
                model, torch.nn.CrossEntropyLoss(reduction='sum'), exercise, 
                metrics_fn=torchmetrics.classification.MulticlassAccuracy(
                    num_classes=10, average='micro'))
        elif exercise == 4:
            score = eval_model(
                model, torch.nn.CrossEntropyLoss(reduction='sum'), exercise, 
                metrics_fn=torchmetrics.classification.MulticlassAccuracy(
                    num_classes=10, average='micro'))

        col, _ = find_cell(self.leaderboard, f'Ejercicio {exercise}')
        self.leaderboard.update_cell(self.__row, col, score)
        self.leaderboard.update_cell(self.__row, col+1, __generate_hash(self.user_id, score, 'pic_uc3m_77'))
        print(f'Score: {score:.5f} submitted to exercise {exercise}')


def __generate_hash(user_id, score, secret_key):
    data = f"{user_id}:{score}:{secret_key}"
    hash_code = hashlib.sha256(data.encode()).hexdigest()
    return hash_code

def __verify_hash(user_id, score, secret_key, hash_code):
    expected_hash = __generate_hash(user_id, score, secret_key)
    return expected_hash == hash_code


def eval_model(model, loss_fn, exercise, metrics_fn=None):
    dataloader = load_data(exercise=exercise)
    device = next(model.parameters()).device
    model.eval()
    loss = 0
    if metrics_fn:
        metrics_fn.to(device)
        metrics_fn.reset()
    with torch.no_grad():
        print(f'Evaluating...')
        for x, y in tqdm(dataloader):
            x, y = x.to(device), y.to(device)
            y_pred = model(x)
            loss += loss_fn(y_pred, y)
            if metrics_fn:
                metrics_fn.update(y_pred, y)
    if metrics_fn:
        return metrics_fn.compute().item()
    else:
        return loss.item() / len(dataloader.dataset)


def load_data(exercise):
    if exercise == 0:
        true_w = torch.tensor([5.0, -16.0, 12.0])
        true_b = torch.Tensor([0.5])
        noise = 0.1
        features, labels = synthetic_data(true_w, true_b, noise, 100000)
        dataset = torch.utils.data.TensorDataset(features, labels)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=100, 
                                                 shuffle=True)
    elif exercise == 1:
        batch_size = 32
        transf = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor()
        ])
        mnist_path = os.path.join(uc3m_pic.__path__[0], '..', 'data')
        mnist_test = torchvision.datasets.FashionMNIST(
            root=mnist_path, train=False, transform=transf, download=True)
        dataloader = torch.utils.data.DataLoader(mnist_test, batch_size,
                                                shuffle=False, num_workers=4)
    elif exercise == 2:
        batch_size = 64
        transform = torchvision.transforms.Compose([
            lambda img: torchvision.transforms.functional.rotate(img, -90),
            lambda img: torchvision.transforms.functional.hflip(img),
            torchvision.transforms.ToTensor()
        ])
        data_path = os.path.join(uc3m_pic.__path__[0], '..', 'data')
        emnist_test = torchvision.datasets.EMNIST(
            root=data_path, split='balanced', train=False, transform=transform, 
            download=True)
        dataloader = torch.utils.data.DataLoader(emnist_test, batch_size,
                                                shuffle=False, num_workers=0)
    elif exercise == 3:
        batch_size = 16
        transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor()
        ])
        data_path = os.path.join(uc3m_pic.__path__[0], '..', 'data')
        eurosat_dataset = torchvision.datasets.EuroSAT(
            root=data_path, transform=transform, 
            download=True)
        strat_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
        _, test_idx = next(strat_split.split(eurosat_dataset, eurosat_dataset.targets))
        test_dataset = torch.utils.data.Subset(eurosat_dataset, test_idx)
        dataloader = torch.utils.data.DataLoader(test_dataset, batch_size,
                                                shuffle=False, num_workers=0)
    elif exercise == 4:
        batch_size = 16
        transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Resize((320, 425), antialias=True)
        ])
        data_path = os.path.join(uc3m_pic.__path__[0], '..', 'data')
        test_path = os.path.join(uc3m_pic.__path__[0], '..', 'data', 'imagenette2-320', 'val')
        test_dataset = torchvision.datasets.ImageFolder(
            root=test_path, transform=transform)
        dataloader = torch.utils.data.DataLoader(test_dataset, batch_size,
                                                        shuffle=False, num_workers=0)
    else:
        raise ValueError('Exercise number not valid')
    
    return dataloader




def synthetic_data(w, b, noise, num_examples):
    x, _ = torch.sort(torch.rand(num_examples))
    y = torch.matmul(torch.stack([x, x**2, x**3]).T, w) + b
    y += torch.normal(0, noise, y.shape)
    return x.unsqueeze(-1), y.unsqueeze(-1)