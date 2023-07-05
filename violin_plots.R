library(tidyverse)
library(ggpubr)
library(rstatix)

# Read the CSV files
sopc <- read.csv("Results/r_sopc.csv")
dppc <- read.csv("Results/r_dppc.csv")

# Read the grouth rate as a list
growth_rate_fluid <- sopc$r
growth_rate_fixed <- dppc$r

# Define the data frame
df <- data.frame(
  growth_rate = c(growth_rate_fluid, growth_rate_fixed),
  slb = rep(c("Fluid", "Fixed"), times = c(length(growth_rate_fluid), length(growth_rate_fixed))),
  Mobility = rep(c("Fluid", "Fixed"), times = c(length(growth_rate_fluid), length(growth_rate_fixed)))
)

# Statistical test
stat.test <- df %>%
  wilcox_test(growth_rate ~ slb) %>%
  add_significance()

violins <- ggviolin(df, x="slb", y="growth_rate", fill="Mobility", color="Mobility", add = "jitter", alpha = 0.2) +
  scale_x_discrete(limits = c("Fluid", "Fixed")) +
  scale_color_manual(values = c("#cf44cd","#4542cf")) +
  theme_bw() + 
  theme(legend.position="none", axis.text = element_text(size = rel(1.2)), axis.title = element_text(size = rel(1.3))) +
  labs(x="SLB", y="Growth Rate [1/S]")

violins +
  stat_pvalue_manual(stat.test, label = "P = {p}", y.position = 0.001) +
  scale_y_continuous(trans = "log10")

ggsave("violin_comparison.png", height = 5, width = 6)