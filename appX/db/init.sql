CREATE DATABASE citiesData;
use citiesData;

CREATE TABLE IF NOT EXISTS tblCitiesImport (
    `id` int AUTO_INCREMENT,
    `fldheight` NUMERIC(4, 2),
    `fldweight` NUMERIC(5, 2),
    PRIMARY KEY (`id`)
);
INSERT INTO tblCitiesImport (fldheight,fldweight) VALUES
    (65.78,112.99),
    (71.52,136.49),
    (69.40,153.03),
    (68.22,142.34),
    (67.79,144.30),
    (68.70,123.30),
    (69.80,141.49),
    (70.01,136.46),
    (67.90,112.37),
    (66.78,120.67),
    (66.49,127.45),
    (67.62,114.14),
    (68.30,125.61),
    (67.12,122.46),
    (68.28,116.09),
    (71.09,140.00),
    (66.46,129.50),
    (68.65,142.97),
    (71.23,137.90),
    (67.13,124.04),
    (67.83,141.28),
    (68.88,143.54),
    (63.48,97.90),
    (68.42,129.50),
    (67.63,141.85),
    (67.21,129.72),
    (70.84,142.42),
    (67.49,131.55),
    (66.53,108.33),
    (65.44,113.89),
    (69.52,103.30),
    (65.81,120.75),
    (67.82,125.79),
    (70.60,136.22),
    (71.80,140.10),
    (69.21,128.75),
    (66.80,141.80),
    (67.66,121.23),
    (67.81,131.35),
    (64.05,106.71),
    (68.57,124.36),
    (65.18,124.86),
    (69.66,139.67),
    (67.97,137.37),
    (65.98,106.45),
    (68.67,128.76),
    (66.88,145.68),
    (67.70,116.82),
    (69.82,143.62),
    (69.09,134.93),
    (69.91,147.02),
    (67.33,126.33),
    (70.27,125.48),
    (69.10,115.71),
    (65.38,123.49),
    (70.18,147.89),
    (70.41,155.90),
    (66.54,128.07),
    (66.36,119.37),
    (67.54,133.81),
    (66.50,128.73),
    (69.00,137.55),
    (68.30,129.76),
    (67.01,128.82),
    (70.81,135.32),
    (68.22,109.61),
    (69.06,142.47),
    (67.73,132.75),
    (67.22,103.53),
    (67.37,124.73),
    (65.27,129.31),
    (70.84,134.02),
    (69.92,140.40),
    (64.29,102.84),
    (68.25,128.52),
    (66.36,120.30),
    (68.36,138.60),
    (65.48,132.96),
    (69.72,115.62),
    (67.73,122.52),
    (68.64,134.63),
    (66.78,121.90),
    (70.05,155.38),
    (66.28,128.94),
    (69.20,129.10),
    (69.13,139.47),
    (67.36,140.89),
    (70.09,131.59),
    (70.18,121.12),
    (68.23,131.51),
    (68.13,136.55),
    (70.24,141.49),
    (71.49,140.61),
    (69.20,112.14),
    (70.06,133.46),
    (70.56,131.80),
    (66.29,120.03),
    (63.43,123.10),
    (66.77,128.14),
    (68.89,115.48);