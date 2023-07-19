# CHANGELOG - ssh_check

## 2.3.3 / 2023-01-20 / Agent 7.43.0

* [Fixed] Update dependencies. See [#13726](https://github.com/DataDog/integrations-core/pull/13726).

## 2.3.2 / 2022-08-05 / Agent 7.39.0

* [Fixed] Dependency updates. See [#12653](https://github.com/DataDog/integrations-core/pull/12653).

## 2.3.1 / 2022-05-15 / Agent 7.37.0

* [Fixed] Upgrade dependencies. See [#11958](https://github.com/DataDog/integrations-core/pull/11958).

## 2.3.0 / 2022-04-05 / Agent 7.36.0

* [Added] Upgrade dependencies. See [#11726](https://github.com/DataDog/integrations-core/pull/11726).
* [Added] Add metric_patterns options to filter all metric submission by a list of regexes. See [#11695](https://github.com/DataDog/integrations-core/pull/11695).

## 2.2.0 / 2022-02-19 / Agent 7.35.0

* [Added] Add `pyproject.toml` file. See [#11439](https://github.com/DataDog/integrations-core/pull/11439).
* [Fixed] Fix namespace packaging on Python 2. See [#11532](https://github.com/DataDog/integrations-core/pull/11532).

## 2.1.1 / 2022-01-08 / Agent 7.34.0

* [Fixed] Add comment to autogenerated model files. See [#10945](https://github.com/DataDog/integrations-core/pull/10945).

## 2.1.0 / 2021-10-04 / Agent 7.32.0

* [Added] Update dependencies. See [#10258](https://github.com/DataDog/integrations-core/pull/10258).
* [Added] Disable generic tags. See [#10027](https://github.com/DataDog/integrations-core/pull/10027).

## 2.0.0 / 2021-08-22 / Agent 7.31.0

* [Fixed] Fix typos in log lines. See [#9907](https://github.com/DataDog/integrations-core/pull/9907).
* [Changed] Remove messages for integrations for OK service checks. See [#9888](https://github.com/DataDog/integrations-core/pull/9888).

## 1.12.0 / 2021-07-12 / Agent 7.30.0

* [Added] Add runtime configuration validation. See [#8989](https://github.com/DataDog/integrations-core/pull/8989).

## 1.11.4 / 2021-03-07 / Agent 7.27.0

* [Fixed] Bump minimum base package version. See [#8443](https://github.com/DataDog/integrations-core/pull/8443).

## 1.11.3 / 2020-09-24 / Agent 7.23.0

* [Fixed] Add integration test for ssh keypair and make code more accurate. See [#7655](https://github.com/DataDog/integrations-core/pull/7655).

## 1.11.2 / 2020-09-21

* [Fixed] pass the password to be used for pkey decryption. See [#6862](https://github.com/DataDog/integrations-core/pull/6862).

## 1.11.1 / 2020-06-29 / Agent 7.21.0

* [Fixed] Add config specs. See [#6923](https://github.com/DataDog/integrations-core/pull/6923).
* [Fixed] Agent6 style init. See [#6924](https://github.com/DataDog/integrations-core/pull/6924).

## 1.11.0 / 2020-05-17 / Agent 7.20.0

* [Added] Allow optional dependency installation for all checks. See [#6589](https://github.com/DataDog/integrations-core/pull/6589).

## 1.10.1 / 2020-04-04 / Agent 7.19.0

* [Fixed] Update deprecated imports. See [#6088](https://github.com/DataDog/integrations-core/pull/6088).

## 1.10.0 / 2020-01-13 / Agent 7.17.0

* [Added] Use lazy logging format. See [#5377](https://github.com/DataDog/integrations-core/pull/5377).
* [Added] Add version metadata. See [#5016](https://github.com/DataDog/integrations-core/pull/5016).

## 1.9.0 / 2019-10-09 / Agent 6.15.0

* [Added] Upgrade Paramiko to version 2.6.0. See [#4685](https://github.com/DataDog/integrations-core/pull/4685). Thanks [daniel-savo](https://github.com/daniel-savo).

## 1.8.0 / 2019-08-24 / Agent 6.14.0

* [Fixed] Remove unused dependencies. See [#4405](https://github.com/DataDog/integrations-core/pull/4405).
* [Added] Upgrade pyasn1. See [#4289](https://github.com/DataDog/integrations-core/pull/4289).

## 1.7.0 / 2019-07-04 / Agent 6.13.0

* [Added] Update cryptography version. See [#4000](https://github.com/DataDog/integrations-core/pull/4000).

## 1.6.0 / 2019-05-14 / Agent 6.12.0

* [Added] Adhere to code style. See [#3569](https://github.com/DataDog/integrations-core/pull/3569).

## 1.5.0 / 2019-01-04 / Agent 6.9.0

* [Added] Support Python 3. See [#2836](https://github.com/DataDog/integrations-core/pull/2836).

## 1.4.0 / 2018-11-30 / Agent 6.8.0

* [Added] Upgrade cryptography. See [#2659](https://github.com/DataDog/integrations-core/pull/2659).

## 1.3.1 / 2018-09-04 / Agent 6.5.0

* [Fixed] Update cryptography to 2.3. See [#1927](https://github.com/DataDog/integrations-core/pull/1927).
* [Fixed] Add data files to the wheel package. See [#1727](https://github.com/DataDog/integrations-core/pull/1727).

## 1.3.0 / 2018-06-20 / Agent 6.4.0

* [Changed] Bump requests to 2.19.1. See [#1743](https://github.com/DataDog/integrations-core/pull/1743).

## 1.2.0 / 2018-03-23

* [FEATURE] Add custom tag support.

## 1.1.3 / 2018-01-10

* [BUGFIX] Check that the private_key_file exists in the yaml configuration before attempting to access it. See [#988](https://github.com/DataDog/integrations-core/issues/988)

## 1.1.2 / 2017-11-21

* [BUGFIX] If `ssh_check` passes and uses `None` as `exception_message`, downstream aggregator rejects it with a type error.
  Instead, specify a default message. See [#852](https://github.com/DataDog/integrations-core/issues/852)

## 1.1.1 / 2017-08-28

* [IMPROVEMENT] drop dependency on winrandom_ctypes for windows

## 1.1.0 / 2017-07-18

* [IMPROVEMENT] Drop dependency on pycrypto. See [#426](https://github.com/DataDog/integrations-core/issues/426) and [#454](https://github.com/DataDog/integrations-core/issues/454)
* [BUGFIX] Fix misplaced parentheses in config validation. See [#416](https://github.com/DataDog/integrations-core/issues/416), thanks [@ilkka](https://github.com/ilkka)

## 1.0.0 / 2017-03-22

* [FEATURE] adds ssh_check integration.