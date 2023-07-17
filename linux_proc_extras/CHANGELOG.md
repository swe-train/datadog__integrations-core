# CHANGELOG - linux_proc_extras

## 2.3.1 / 2023-07-10

***Fixed***:

* Bump Python version from py3.8 to py3.9. See [#14701](https://github.com/DataDog/integrations-core/pull/14701).

## 2.3.0 / 2022-04-05 / Agent 7.36.0

***Added***:

* Add metric_patterns options to filter all metric submission by a list of regexes. See [#11695](https://github.com/DataDog/integrations-core/pull/11695).

## 2.2.0 / 2022-02-19 / Agent 7.35.0

***Added***:

* Add `pyproject.toml` file. See [#11391](https://github.com/DataDog/integrations-core/pull/11391).

***Fixed***:

* Fix namespace packaging on Python 2. See [#11532](https://github.com/DataDog/integrations-core/pull/11532).

## 2.1.1 / 2022-01-08 / Agent 7.34.0

***Fixed***:

* Add comment to autogenerated model files. See [#10945](https://github.com/DataDog/integrations-core/pull/10945).

## 2.1.0 / 2021-10-04 / Agent 7.32.0

***Added***:

* Add runtime configuration validation. See [#8949](https://github.com/DataDog/integrations-core/pull/8949).

## 2.0.1 / 2021-03-07 / Agent 7.27.0

***Fixed***:

* Bump minimum base package version. See [#8443](https://github.com/DataDog/integrations-core/pull/8443).

## 2.0.0 / 2020-09-09 / Agent 7.22.1

***Changed***:

* Put interrupt metrics behind a config option. See [#7553](https://github.com/DataDog/integrations-core/pull/7553).

## 1.4.0 / 2020-08-10 / Agent 7.22.0

***Added***:

* Adding interrupts stats. See [#7166](https://github.com/DataDog/integrations-core/pull/7166).

## 1.3.0 / 2020-05-17 / Agent 7.20.0

***Added***:

* Allow optional dependency installation for all checks. See [#6589](https://github.com/DataDog/integrations-core/pull/6589).

## 1.2.1 / 2020-04-04 / Agent 7.19.0

***Fixed***:

* Update deprecated imports. See [#6088](https://github.com/DataDog/integrations-core/pull/6088).

## 1.2.0 / 2019-05-14 / Agent 6.12.0

***Added***:

* Adhere to code style. See [#3534](https://github.com/DataDog/integrations-core/pull/3534).

## 1.1.0 / 2019-01-04 / Agent 6.9.0

***Added***:

* Support Python 3. See [#2852][1].

## 1.0.1 / 2018-09-04 / Agent 6.5.0

***Fixed***:

* Add data files to the wheel package. See [#1727][2].

## 1.0.0 / 2017-03-22

***Added***:

* adds linux_proc_extras integration.

[1]: https://github.com/DataDog/integrations-core/pull/2852
[2]: https://github.com/DataDog/integrations-core/pull/1727