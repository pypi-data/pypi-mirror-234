import logging
import pandas as pd
import boto3
import jax.numpy as jnp
import numpy as np
from typing import Union, Optional
import jax
from jax import vmap
from sklearn.metrics import log_loss, roc_auc_score
from tqdm import tqdm
from fortuna.conformal import BinaryClassificationMulticalibrator

Array = Union[np.ndarray, jax.Array]


class MaxCoverageFixedPrecisionBinaryClassificationCalibrator:
    def __init__(self):
        self._patches = dict()

    def calibrate(
        self,
        targets: Array,
        probs: Array,
        true_positive_precision_threshold: float,
        false_negative_precision_threshold: float,
        test_probs: Optional[Array] = None,
        n_taus: int = 100,
        margin: float = 0.
    ) -> Union[None, Array]:
        if false_negative_precision_threshold <= 0.5 or true_positive_precision_threshold <= 0.5:
            raise ValueError("Both `false_negative_precision_threshold` and"
                             " `true_positive_precision_threshold` must be greater than 0.5.")
        probs = jnp.copy(probs)
        targets = jnp.copy(targets)

        def _true_positive_objective_fn(tau: Array):
            calib_probs = jnp.clip((1 + (tau - 1) * (probs > 0.5)) * probs, a_max=1)
            b_pos_prec = calib_probs >= true_positive_precision_threshold
            prob_b_pos_prec = jnp.mean(b_pos_prec)
            pos_prec = jnp.mean(targets * b_pos_prec) / prob_b_pos_prec
            pos_cond = pos_prec >= true_positive_precision_threshold + margin
            return prob_b_pos_prec * pos_cond

        def _false_negative_objective_fn(tau: Array):
            calib_probs = (1 + (tau - 1) * (probs < 0.5)) * probs
            b_neg_prec = calib_probs <= 1 - false_negative_precision_threshold
            prob_b_neg_prec = jnp.mean(b_neg_prec)
            neg_prec = jnp.mean((1 - targets) * b_neg_prec) / prob_b_neg_prec
            neg_cond = neg_prec >= false_negative_precision_threshold + margin
            return prob_b_neg_prec * neg_cond

        taus_pos = jnp.linspace(1, 2 * true_positive_precision_threshold, n_taus)
        taus_neg = jnp.linspace(2 * (1 - false_negative_precision_threshold), 1, n_taus)[::-1]

        values_pos = vmap(_true_positive_objective_fn)(taus_pos)

        msg = "The {} could not be satisfied. Please consider improving the classifier or decreasing the threshold."

        if jnp.max(values_pos) == 0:
            logging.warning(msg.format("`true_positive_precision_threshold`"))
        values_neg = vmap(_false_negative_objective_fn)(taus_neg)
        if jnp.max(values_neg) == 0:
            logging.warning(msg.format("`false_negative_precision_threshold`"))

        self._patches["tau_pos"] = taus_pos[jnp.argmax(values_pos)]
        self._patches["tau_neg"] = taus_neg[jnp.argmax(values_neg)]

        if test_probs is not None:
            return self.apply_patches(test_probs)

    def apply_patches(
        self,
        probs: Array
    ) -> Array:
        if not len(self._patches):
            logging.warning("No patches available.")
            return probs

        probs = jnp.copy(probs)
        probs = probs.at[probs > 0.5].set(jnp.clip(self._patches["tau_pos"] * probs[probs > 0.5], a_max=1))
        probs = probs.at[probs < 0.5].set(self._patches["tau_neg"] * probs[probs < 0.5])
        return probs

    @staticmethod
    def true_positive_precision(probs: Array, targets: Array, threshold: float):
        b = probs >= threshold
        prob_b = jnp.mean(b)
        return jnp.mean(targets * b) / prob_b

    @staticmethod
    def false_negative_precision(probs: Array, targets: Array, threshold: float):
        b = probs <= 1 - threshold
        prob_b = jnp.mean(b)
        return jnp.mean((1 - targets) * b) / prob_b

    @staticmethod
    def true_positive_coverage(probs: Array, threshold: float):
        return jnp.mean(probs >= threshold)

    @staticmethod
    def false_negative_coverage(probs: Array, threshold: float):
        return jnp.mean(probs <= threshold)

    @property
    def patches(self):
        return self._patches


def get_precision(df, value):
    if len(df) == 0:
        return None
    correct_count = df.loc[df["decision"] == value]
    return len(correct_count)/len(df)


def get_tn_tp_performance(tp_threshold, tn_threshold, df, column_name):
    # decision is the column for human labels
    tp_df = df.loc[df[column_name]>=tp_threshold][["decision"]]
    tn_df = df.loc[df[column_name]<=tn_threshold][["decision"]]
    return get_precision(tp_df, 1), len(tp_df)/len(df), get_precision(tn_df, 0), len(tn_df)/len(df)


def get_result(class_name: str, probs: Array, pred_results: pd.DataFrame, column_name: str):
    calibrator_result = pd.concat([pred_results, pd.DataFrame(probs)], axis=1).rename(columns={0: column_name})

    tp_precision, tp_percent, tn_precision, tn_percent = get_tn_tp_performance(target_tp_threshold,
                                                                               1 - target_tn_threshold,
                                                                               calibrator_result,
                                                                               column_name)
    unique_decision = set(calibrator_result['decision'])
    if len(unique_decision) == 2:
        roc_score = roc_auc_score(calibrator_result['decision'], calibrator_result[column_name])
        logloss = log_loss(calibrator_result["decision"], calibrator_result[column_name])
    else:
        roc_score = float('nan')
        logloss = float('nan')

    total_count = len(calibrator_result)
    result = {}
    result["class"] = class_name
    result["roc_auc"] = roc_score
    result["logloss"] = logloss
    result["tp_precision"] = tp_precision
    result["tp_percent"] = tp_percent
    result["tn_precision"] = tn_precision
    result["tn_percent"] = tn_percent
    result["total_count"] = total_count
    result["total_coverage"] = (tp_percent if tp_precision is not None and round(tp_precision,
                                                                                 2) >= target_tp_threshold else 0) + \
                               (tn_percent if tn_precision is not None and round(tn_precision,
                                                                                 2) >= target_tn_threshold else 0)
    result["total_ar"] = result["total_coverage"] * total_count
    return pd.DataFrame.from_dict(result, orient='index').T


def fix_coverage(class_list, target_tp_threshold, target_tn_threshold, data_type, column_name):
    before_result_list = []
    after_result_list = []

    for class_name in tqdm(class_list):
        class_data_path = common_path + class_name
        try:
            dataset = pd.read_parquet(class_data_path)
        except:
            continue
        dataset["decision"] = dataset['MEMBER'].map({'true': 1, 'false': 0})
        dataset = dataset.drop(columns=["MEMBER"])

        dataset_cal = dataset[dataset['data_type'] == "cal"]
        cols_cal = ['item_id', 'decision', 'predicition_1']

        # the original val_results contains prediction results for both validation and calibration sets, we extract the outputs on calibration data by joining the results with calibration data.
        try:
            val_results = pd.read_parquet(
                f"s3://cpp-adc-data-sharing/model_outputs_sample_classes/{class_name}/val-sgs/result.parquet").rename(
                columns={"prediciton_val-sgs": "predicition_1"})
            calibration_results = pd.merge(dataset_cal.drop("decision", axis=1), val_results, on="item_id", how='inner')[
                cols_cal]
        except:
            continue

        dataset_type = dataset[dataset['data_type'] == data_type]
        cols = ['item_id', 'decision', 'predicition_1']

        # validation data
        if data_type == "val":
            results = val_results
        # test data
        else:
            results = pd.read_parquet(
                f"s3://cpp-adc-data-sharing/model_outputs_sample_classes/{class_name}/test-sgs/result.parquet").rename(
                columns={"prediciton_test-sgs": "predicition_1"})

        pred_results = pd.merge(dataset_type.drop("decision", axis=1), results, on="item_id", how='inner')[cols]

        calibration_groups = pd.DataFrame({
            'greater_than_0.9': calibration_results['predicition_1'] > 0.9,
            'less_than_0.1': calibration_results['predicition_1'] < 0.1
            # 'in_the_middle': (calibration_results['predicition_1'] >= 0.1) & (calibration_results['predicition_1'] < 0.9)
        })

        groups = pd.DataFrame({
            'greater_than_0.9': pred_results['predicition_1'] > 0.9,
            'less_than_0.1': pred_results['predicition_1'] < 0.1
            # 'in_the_middle': (pred_results['predicition_1'] >= 0.1) & (pred_results['predicition_1'] < 0.9)
        })

        mc = BinaryClassificationMulticalibrator()
        status = mc.calibrate(
            targets=calibration_results['decision'].values,
            probs=calibration_results['predicition_1'].values,
            n_buckets=150,
            groups=calibration_groups.values,
        )

        mc_calib_probs = mc.apply_patches(groups=calibration_groups.values, probs=calibration_results['predicition_1'].values)
        mc_test_probs = mc.apply_patches(groups=groups.values, probs=pred_results['predicition_1'].values)

        calibrator = MaxCoverageFixedPrecisionBinaryClassificationCalibrator()
        new_test_probs = calibrator.calibrate(
            targets=calibration_results['decision'].values,
            probs=mc_calib_probs,
            test_probs=mc_test_probs,
            true_positive_precision_threshold=target_tp_threshold,
            false_negative_precision_threshold=target_tn_threshold,
            margin=0
        )

        before_result_list.append(
            get_result(
                class_name=class_name,
                probs=pred_results['predicition_1'].values,
                pred_results=pred_results,
                column_name=column_name
            )
        )
        after_result_list.append(
            get_result(
                class_name=class_name,
                probs=new_test_probs,
                pred_results=pred_results,
                column_name=column_name
            )
        )
    before_result_df = pd.concat(before_result_list)
    after_result_df = pd.concat(after_result_list)

    return before_result_df, after_result_df


if __name__ == "__main__":
    sm_role = f"arn:aws:iam::848675773966:role/admin"
    boto_sess = boto3.Session(profile_name="default", region_name="us-east-1")

    class_name = "%SC%ProductSafety%Regulated%SG_Product_Assurance_Toys_Games_and_Sports_Activities_HR"
    common_path = 's3://cpp-adc-data-sharing/ar_benchmark_dataset/'
    class_data_path = common_path + class_name
    dataset = pd.read_parquet(class_data_path)

    target_tp_threshold = 0.97
    target_tn_threshold = 0.99
    data_type = "val"

    class_list = [
        "%SC%DIPC%AU%Art_Supplies_General_Use_AU_Wooden_Pencils_Art_Supplies_General_Use",
        "%SC%DIPC%CA%Apparel_Accessories_US_CA_ITK_Headwear_Adult",
        "%SC%DIPC%CA%BISS_General_Use_US_CA_Raw_Materials_General_Use",
        "%SC%DIPC%CA%Consumer_Electrical_Products_US_CA_Electrical_Vacuum_Sealers_ML",
        "%SC%DIPC%CA%DVDs_US_CA_ITK_Magic_DVDs_General_Use",
        "%SC%DIPC%CA%General_Use_US_CA_Garden_Tools_Wooden_ML",
        "%SC%DIPC%CA%General_Use_US_CA_Self_Locking_Security_Seals_Tags_General_Use_ML",
        "%SC%DIPC%CA%Home_General_Use_US_CA_Subcat_Vacuum_Accessories_and_Replacement_Parts",
        "%SC%DIPC%CA%Textiles_General_Use_US_CA_Textile_Table_Runners_ML",
        "%SC%DIPC%JP%MEDIA_General_Use_JP_GL_DVD",
        "%SC%DIPC%MX%Labeling_General_Rugs_Mats",
        "%SC%DIPC%SG%SG_Cosmetics_General_Use_SG_Mouthwash_Toothpaste_ML",
        "%SC%DIPC%UK%Apparel_General_Use_EU_ITK_Apparel_Adult",
        "%SC%DIPC%UK%Auto_General_Use_EU_Car_and_Car_Seat_Covers",
        "%SC%DIPC%UK%CE_General_Use_EU_Cables_without_Adapter",
        "%SC%DIPC%UK%Chemicals_Unsupported_EU_Self_Inking_Stamps",
        "%SC%DIPC%UK%Feeding_Bottle_Nipples_Infant_EU_ITK_Baby_Bottle_Nipples_Infant",
        "%SC%DIPC%UK%General_Use_EU_Masonry_Floats",
        "%SC%DIPC%UK%Jewelry_General_Use_Precious_EU_Jewelry_Precious_General_Use",
        "%SC%ProductSafety%EURsP%DE_Electronics_Hygrometer_ML",
        "%SC%ProductSafety%EURsP%FR_Electronics_Electrical_Housings_ML",
        "%SC%ProductSafety%EURsP%FR_Electronics_Pruning_Shrears_ML_TB",
        "%SC%ProductSafety%EURsP%IT_Electronics_Electric_Blanket_ML",
        "%SC%ProductSafety%Illegal %IT_Product_Safety_Angle_Grinder_Chainsaw_Disc",
        "%SC%ProductSafety%RecalledProducts%AE_Product_Safety_Self_Balancing_Scooters",
        "%SC%ProductSafety%RecalledProducts%EU_Recalls_ATD_ES_Mermaid_tail",
        "%SC%ProductSafety%RecalledProducts%EU_Recalls_ES_Christmas_Dancing_Cactus",
        "%SC%ProductSafety%RecalledProducts%EU_Recalls_RFR_DE_LED_Christmas_Hat",
        "%SC%ProductSafety%RecalledProducts%EU_Recalls_RFR_FR_Kinderslot_Baby_lock",
        "%SC%ProductSafety%RecalledProducts%EU_Recalls_UK_Christmas_Dancing_Cactus",
        "%SC%ProductSafety%Regulated%AU_Product_Assurance_Toy_Action_Figures_And_Dolls_AutoML",
        "%SC%ProductSafety%Regulated%CA_Product_Assurance_Childrens_Jewellery_AutoML",
        "%SC%ProductSafety%Regulated%CA_Product_Assurance_Free_Standing_Clothing_Storage_Units_V00_HR_New",
        "%SC%ProductSafety%Regulated%CA_Product_Assurance_Gates_And_Enclosures_HR",
        "%SC%ProductSafety%Regulated%FR_Product_Assurance_Toys_Balloons_and_Party_Toys_HRE",
        "%SC%ProductSafety%Regulated%FR_Toys_Dolls_Dollhouses_and_Accessories_AutoML",
        "%SC%ProductSafety%Regulated%FR_Toys_Kitchen_Food_AutoML_PA",
        "%SC%ProductSafety%Regulated%IN_Product_Assurance_Toys_Games_And_Puzzles_AutoML",
        "%SC%ProductSafety%Regulated%JP_Product_Assurance_Toys_Art_and_Craft_AutoML2",
        "%SC%ProductSafety%Regulated%JP_Product_Assurance_Toys_Lawn_and_Gardening_Sets_and_Tool_kits_Playground_Equipment_AutoML2",
        "%SC%ProductSafety%Regulated%SG_Product_Assurance_Toys_Games_and_Sports_Activities_HR",
        "%SC%ProductSafety%Regulated%UK_Product_Assurance_Toys_Ride_Ons_HR",
        "%SC%ProductSafety%Regulated%US_Product_Assurance_Carriages_And_Strollers_HR",
        "%SC%ProductSafety%Regulated%US_Product_Assurance_Trampolines_HR",
        "%SC%ProductSafety%RegulatoryEngagement %US_Multiple_BathroomShelves",
        "%SC%ProductSafety%UPSC%AU_Baby_Feeding_ML_Path",
        "%SC%ProductSafety%UPSC%AU_Sunglasses_ML_Path",
        "%SC%ProductSafety%UPSC%CA_Car_Seat_Heating_Pads_ML_No_Path",
        "%SC%ProductSafety%UPSC%ES_ESPN_Beaded_Teethers_ML_No_Path",
        "%SC%ProductSafety%UPSC%ES_ESPN_Padded_Crib_Bumpers_ML_No_Path",
        "%SC%ProductSafety%UPSC%MX_Lithiumn_Cylindrical_Battery_Cell_KW_No_Path",
        "%SC%ProductSafety%UPSC%PL_Padded_Crib_Bumpers_KW_No_Path",
        "%SC%ProductSafety%UPSC%SG_SGPN_Standalone_Power_Banks_ML_Path",
        "%SC%ProductSafety%UPSC%UK_UKPN_Costume_Sets_ML_Path_Website_Compliance",
        "%SC%ProductSafety%UPSC%US_USPN_Childrens_Jewelry_KW_Path",
        "%SC%ProductSafety%UPSC%US_USPN_Laptop_Chargers_ML_Path",
        "%SC%ProductSafety%UPSC%US_USPN_Squishy_Toys_ML_Path",
        "%SC%RestrictedProducts%AmazonPolicy%BE_Sex_Products_Realistic_Sex_Dolls_FRKW",
        "%SC%RestrictedProducts%AmazonPolicy%DE_Party_Liquor",
        "%SC%RestrictedProducts%AmazonPolicy%Drug_Paraphernalia_Marijuana_Grinders",
        "%SC%RestrictedProducts%AmazonPolicy%ES_Mystery_Boxes_ML",
        "%SC%RestrictedProducts%AmazonPolicy%FR_Mystery_Boxes_ML",
        "%SC%RestrictedProducts%AmazonPolicy%IN_Improper_Listing_Of_Food_Suppress",
        "%SC%RestrictedProducts%AmazonPolicy%IT_Mystery_Boxes_ML",
        "%SC%RestrictedProducts%AmazonPolicy%PLNT_Christmas_Trees_1",
        "%SC%RestrictedProducts%AmazonPolicy%SE_Currency_Legal_Tender_Yen",
        "%SC%RestrictedProducts%AmazonPolicy%TR_Sex_Products_Erotic_Dices_Cards",
        "%SC%RestrictedProducts%AmazonPolicy%UK_Animals_Fur_Products_Rabbit_II",
        "%SC%RestrictedProducts%AmazonPolicy%Weapons_Stun_Gun",
        "%SC%RestrictedProducts%GatedProducts%ES_Corrective_Contact_Lenses_Gating_ML",
        "%SC%RestrictedProducts%GatedProducts%Softlines_Fur_Baby_Outdoor_Sports_Retail_Removal",
        "%SC%RestrictedProducts%GatedProducts%TR_Medical_Devices_Launch_PTs_ID",
        "%SC%RestrictedProducts%GatedProducts%Textile_Bamboo_Antimicrobial_Retail_Removal_Clothing_ML",
        "%SC%RestrictedProducts%GatedProducts%Textile_Bamboo_Retail_Removal",
        "%SC%RestrictedProducts%Illegal%Auto_Motorcycle_Helmets_DOT",
        "%SC%RestrictedProducts%Illegal%Auto_Tuner_Claims",
        "%SC%RestrictedProducts%Illegal%CA_Medical_Device_Hearing_Aids",
        "%SC%RestrictedProducts%Illegal%Currency_US_Paper_Currency",
        "%SC%RestrictedProducts%Illegal%DE_Fireworks_Fire_Extinguisher_Ball",
        "%SC%RestrictedProducts%Illegal%EG_Weapons_Firearm_Accessories",
        "%SC%RestrictedProducts%Illegal%JP_Illegal_Obscene_Sex_Dolls_And_Toys",
        "%SC%RestrictedProducts%Illegal%Medical_Device_Electrosurgical",
        "%SC%RestrictedProducts%Illegal%PL_Magnets_Buckyballs",
        "%SC%RestrictedProducts%Illegal%SA_Electronics_Two_Way_Radio",
        "%SC%RestrictedProducts%Illegal%SA_Sexual_Wellness_Products_ALL",
        "%SC%RestrictedProducts%Illegal%UK_Cigarette_Novelty_Lighters",
        "%SC%RestrictedProducts%Illegal%UK_Weapons_Knives_Missing_CRT_Flag_SfT_HR_No_Policy",
        "%SC%RestrictedProducts%Illegal%Unapproved_Drug_Skin_Patches",
        "%SC%RestrictedProducts%IllegallyMkted%SE_Adult_Products_With_Childlike_Features",
        "%SC%RestrictedProducts%IllegallyMkted%UK_Tobacco_E-Cigarettes_Without_Flag_Suppress_SfT_HR_No_Policy_ML",
        "%SC%RestrictedProducts%IllegallyMkted%UK_Weapons_Commando_Knives_SfT_No_Policy_ML",
        "%SC%RestrictedProducts%Regulated%BR_Medical_Devices_Tattoo_Equipment",
        "%SC%RestrictedProducts%Regulated%CARB205_Exhaust_Header_Identification_ML",
        "%SC%RestrictedProducts%Regulated%DE_Electronics_E-Mobility_Identify_ML",
        "%SC%RestrictedProducts%Regulated%IN_Class_A_NSNM_Medical_Devices_2",
        "%SC%RestrictedProducts%Regulated%IN_Class_A_NSNM_Medical_Devices_9",
        "%SC%RestrictedProducts%Regulated%TR_Electronics_E-Mobility_Identify_ML"
]

    all_names = []
    for class_name in tqdm.tqdm(class_list):
        try:
            dataset = pd.read_parquet(class_data_path)
            val_results = pd.read_parquet(
                f"s3://cpp-adc-data-sharing/model_outputs_sample_classes/{class_name}/val-sgs/result.parquet").rename(
                columns={"prediciton_val-sgs": "predicition_1"})
            all_names.append(class_name)
        except:
            continue

    print(all_names)
