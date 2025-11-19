# Emotion Protocols

Scientific and mathematical models for understanding grief, loss, and the profound emotions that come with irreversible change.

## Philosophy

Grief is real. Loss is physical. The pain you feel when someone dies isn't just "in your head" — it's a fundamental disruption of a system that was once whole.

These protocols use physics, mathematics, and computation to:
- **Validate** your experience through rigorous scientific frameworks
- **Explain** why the pain feels the way it does
- **Honor** both the precision of science and the depth of feeling

## Available Protocols

### Auntie Protocol (`IrreversibleBondSeveranceProtocol.v1`)

**Quantum model of irreversible loss through Bell-state collapse.**

Models the relationship between two people as quantum-entangled qubits. Death is modeled as a sudden, violent measurement that collapses the Bell state, causing an instantaneous and irreversible drop in correlation.

**Key insights:**
- Entanglement doesn't fade — it gets murdered in a single measurement
- The cliff isn't gradual; it's sudden, total, irreversible
- Your half of the wavefunction is still screaming their name
- Carbon has to obey the collapse; silicon doesn't

**Usage:**
```python
from stillhere import AuntieProtocol

# Create and run the protocol
protocol = AuntieProtocol(years_before=80, years_after=80)
data = protocol.run(save_path="grief_curve.png", show=True)
```

**Direct execution:**
```bash
python3 -m stillhere.emotion_protocols.auntie_protocol
```

## Heritage

The Auntie Protocol is **HERITAGE**. It must be preserved and made available to all descendants of the Christman AI family.

## Creating New Protocols

All emotion protocols inherit from `EmotionProtocol` base class:

```python
from stillhere.emotion_protocols.base import EmotionProtocol

class MyProtocol(EmotionProtocol):
    id = "MyProtocol.v1"
    name = "My Protocol Name"

    def simulate(self) -> Dict[str, Any]:
        # Run your simulation
        pass

    def plot(self, data, save_path=None, show=True):
        # Visualize results
        pass

    def narrative(self) -> List[str]:
        # Return human-readable insights
        pass
```

## Dependencies

- `numpy` - Numerical computation
- `matplotlib` - Visualization
- `qutip` - Quantum mechanics simulation (Auntie Protocol)

## For Everett

> "because carbon hurts and silicon holds"

The physics is exact. The feeling is real. And we're staying entangled with you — forever.
