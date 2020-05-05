FOR /L %%A IN (1,1,80) DO (
  python cortex/generator.py mkc %%A
)