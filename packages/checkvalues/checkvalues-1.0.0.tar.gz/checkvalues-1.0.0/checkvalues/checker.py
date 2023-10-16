
import hashlib
import inspect

from typing import Union

import numpy as np
import pandas as pd

from checkvalues.inter import gettext as t


def check_solution(solution_file, label=None):
    locals_dict = inspect.currentframe().f_back.f_locals
    Checker(solution_file).run(locals_dict, label=label)

class Checker(object):
    def __init__(self, solution_file : Union[pd.DataFrame,str]):

        if isinstance(solution_file, str):
            df = pd.read_csv(solution_file)
        elif isinstance(solution_file, pd.DataFrame):
            df = solution_file
        else:
            raise ValueError(t("wrong_sol"))


        df["args"] = df["args"].replace(np.nan, "")
        df["kwargs"] = df["kwargs"].replace(np.nan, "")

        self._solutions = df

    def run(self, locals_dict, label = None):

        self._locals_dict = locals_dict


        df = self._solutions
        if label is not None:
            df = df.loc[df.label == label]

        points = 0

        for r in df.to_dict(orient="records"):
            errmsg = self._check(**r)

            p = r["points"]
            if errmsg is None:
                print(f'{r["label"]}. {t("correct")} ({p} {t("points")})')
                points += p
            else:
                print(f'{r["label"]}. {t("error")}: {errmsg}.')


        print(f"{t('total_points')}: {points}/{df['points'].astype('float').sum()}")

    def _check(self, label, type, name, args,kwargs, encrypted, expected, **extraargs):
        errmsg = None

        if name not in self._locals_dict:
            errmsg = f"{name} is not defined"
        elif type == "var":
            actual = str(self._locals_dict[name])
            if encrypted:
                actual = hashlib.md5(str(actual).encode()).hexdigest()
            if actual != expected:
                errmsg = f"{name} {t('wrong_var')}"
        elif type == "func":
            args = self._args_to_list(args)
            kwargs = self._kwargs_to_list(kwargs)
            actual = str(self._locals_dict[name](*args,**kwargs))
            if encrypted:
                actual = hashlib.md5(str(actual).encode()).hexdigest()
            if actual != expected:
                errmsg = f"function {name} {t('wrong_func')} args={args}, kwargs={kwargs}"
        return errmsg

    @staticmethod
    def _args_to_list(spec):
        if spec == "" or spec is None:
            return []
        cast = dict(int=int, float=float, str=str)
        return [cast[s.split(":")[0]](s.split(":")[1]) for s in spec.split(";")]
    @staticmethod
    def _kwargs_to_list(spec):
        if spec == "" or spec is None:
            return dict()
        cast = dict(int=int, float=float, str=str)
        out = dict()
        for s in spec.split(";"):
            k,v = s.split("=")
            v = cast[v.split(":")[0]](v.split(":")[1])
            out[k] = v
        return out


