# INTEL TOOLKIT

This library has the function of abstracting and extracting data from APIs such as InTheWild, Strobes_VI and Sploitus, as well as a CVEs prioritization module using the base algorithm of the [CVE_Prioritizer ](https://github.com/TURROKS/CVE_Prioritizer)project, in order to bring insights about CVEs.

## See how the CLI works

[![asciicast](https://asciinema.org/a/XeEM395BAFDYWSnPg0KoMMXmn.svg)](https://asciinema.org/a/XeEM395BAFDYWSnPg0KoMMXmn)

## Installation

With PIP

```bash
pip install intel-toolkit
```

With Poetry

```bash
poetry add intel-toolkit
```

## How to use

### InTheWild - Module

```python
# Import module
import intel_toolkit.inthewild

# Load module
consult = intel_toolkit.inthewild.consult()

# Return feed top exploitation from InTheWild
consult.exploitations_feed()

# Return feed top exploits from InTheWild
consult.exploits_feed()

# Return information about exploits from especific CVE in InTheWild
consult.get_exploit_vuln_id('CVE-2022-22965')

# Return information about exploitation from especific CVE in InTheWild
consult.get_exploitation_vuln_id('CVE-2022-22965')

# Return total exploitations in number_int from especific CVE in InTheWild
consult.get_vuln_total_exploitation('CVE-2022-22965')

# Return total exploits in number_int from especific CVE in InTheWild
consult.get_vuln_total_exploits('CVE-2022-22965')
```

### Strobes_VI

```python
# Import module
import intel_toolkit.strobes_vi

# Load module
consult = intel_toolkit.strobes_vi.consult()

# Return full information about CVE from Strobes_VI
consult.get_vuln_id_info('CVE-2022-22965')

# Return TRUE of FALSE case CVE has Exploit Strobes_VI
consult.check_vuln_has_exploit('CVE-2022-22965')

# Return list references URL from exploits in Strobes_VI
consult.get_refs_vuln_exploits('CVE-2022-22965')

# Return TRUE of FALSE case CVE has Patch Fix Strobes_VI
consult.check_vuln_has_patch('CVE-2022-22965')

# Return list references URL from Patch Fix in Strobes_VI
consult.get_refs_vuln_patch('CVE-2022-22965')

# Returns TRUE from FALSE if CVE was a Zero Day Strobes_VI
consult.check_vuln_is_zeroday('CVE-2022-22965')

# Return list references URL from Zero Day in Strobes_VI
consult.get_refs_vuln_zeroday('CVE-2022-22965')
```

### Sploitus

```python
# Import module
import intel_toolkit.sploitus

# Load module
consult = intel_toolkit.sploitus.consult()

# Return full information about CVE from Sploitus
consult.get_vuln_id_info('CVE-2022-22965')

# Return TRUE of FALSE case CVE has Exploit Sploitus
consult.check_vuln_has_exploit('CVE-2022-22965')

# Return list data about exploits found in Sploitus
consult.get_vuln_exploits('CVE-2022-22965')

# Return total exploits in number_int from especific CVE in Sploitus
consult.get_vuln_total_exploits('CVE-2022-22965')

# Return TRUE of FALSE case CVE has Tools in Sploitus
consult.check_vuln_has_tool('CVE-2022-22965')

# Return list data about tools found in Sploitus
consult.get_vuln_tools('CVE-2022-22965')

# Return total tools in number_int from especific CVE in Sploitus
consult.get_vuln_total_tools('CVE-2022-22965')
```

### CVE_Prioritizer

```python
# Import module
from intel_toolkit.cve_prioritizer import consult

# Load module
consult = consult(api_key_nvd="API_KEY_NVD")

# Calculates the priority of a CVE based on EPSS, CVSS and whether it is present in the CISA_KEY
consult.calc_priority_cve('CVE-2022-22965')

# Does the same as consult.calc_priority_cve but in batch, taking only a list of CVEs as input
consult.process_list(['CVE-2022-22965', 'CVE-2021-3749', 'CVE-2023-0842'])
```
