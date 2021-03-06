#!/usr/bin/env python

import numpy as np
from modelmock.user_info.__seeds import provider
from unidecode import unidecode

class Generator(object):

  def __init__(self, **kwargs):
    self.__uniqset_emails = []
    self.__uniqset_phones = []


  def _generate(self):
    _gender = np.random.choice(["F","M"])
    _first_name, _middle_name, _last_name = self.__generate_name(gender=_gender)
    return dict(
      gender=_gender,
      email=self.__generate_email(_first_name, _middle_name, _last_name),
      phone=self.__generate_phone(),
      fullname=" ".join(filter(lambda s: s is not None and len(s)>0, [_last_name, _middle_name, _first_name]))
    )


  def __generate_name(self, gender):
    if gender == "F":
      return np.random.choice(provider.first_names_female), \
          np.random.choice(provider.middle_name_female), \
          np.random.choice(provider.last_names)

    return np.random.choice(provider.first_names_male), \
        np.random.choice(provider.middle_name_male) if np.random.randint(0,4) else '', \
        np.random.choice(provider.last_names)


  def __generate_email(self, first_name, middle_name, last_name):
    while True:
      _email = unidecode(first_name.lower() \
          + '.' + last_name.lower() \
          + '_' + str(np.random.randint(100, 999)) \
          + '@' + np.random.choice(provider.free_email_domains))
      if _email not in self.__uniqset_emails:
        self.__uniqset_emails.append(_email)
        break
    return _email


  def __generate_phone(self):
    while True:
      _phone = np.random.choice(provider.phone) + ''.join(map(str, np.random.choice(10,8).tolist()))
      if _phone not in self.__uniqset_phones:
        self.__uniqset_phones.append(_phone)
        break
    return _phone


  def inject_user_info(self, nodes):
    for node in nodes:
      node.update(self._generate())
      yield node
