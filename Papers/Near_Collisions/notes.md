# Near collisions

### Complexity Estimates of a SHA-1 Near-Collision Attack for GPU and FPGA

Talks about global 'root certificates' and their use of SHA1.

Paper uses full SHA-1 hash compressions as a unit of measurement.


On the topic of FGPAs

```
For field-programmable gate arrays (FPGA)
algorithms have been designed for 71 and 75 rounds which
claim lowered costs by an order of magnitude
```

They also used the:

```
Xilinx ML605 board
```

Paper states Radeon R9 290x can do 2^31.9 H/s (4007346184)

To compare my RX480 could do similar at 4081000000 H/s

Paper implements the first section of Marc Steven's code to generate near-collisions. His implementation seems to be divisible into 3 phases. 

The probability of a hash meeting the criteria for each stage will determine the work level required.

Marc steven's quotes the work of the near-collisions at `2^57.5`. If this is a measurement of SHA-1 compressions per second it would take one AMD RX480 1.5 years