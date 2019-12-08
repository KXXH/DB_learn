/*
 Navicat Premium Data Transfer

 Source Server         : free_shark
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : free_shark

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 08/12/2019 16:21:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comorder
-- ----------------------------
DROP TABLE IF EXISTS `comorder`;
CREATE TABLE `comorder`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commodity_id` int(11) NOT NULL,
  `buyer_id` int(11) NOT NULL,
  `seller_id` int(11) NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '0-表示未处理，1-表示已同意，2-表示不同意',
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of comorder
-- ----------------------------
INSERT INTO `comorder` VALUES (1, 1, 1, 2, '0', '2019-12-04 13:15:16');
INSERT INTO `comorder` VALUES (2, 5, 2, 3, '0', '2019-12-03 13:15:33');
INSERT INTO `comorder` VALUES (3, 1, 2, 3, '1', '2019-12-08 15:30:41');
INSERT INTO `comorder` VALUES (4, 1, 2, 3, '1', '2019-12-08 15:31:03');

SET FOREIGN_KEY_CHECKS = 1;
