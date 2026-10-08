"""Paper-used subtypes, primary families and derived stages; not run labels."""
_MODES = [
    ('M01_POLARITY_INVERSION','测试极性倒置','任务建模失败','S1'),
    ('M02_TARGET_BEHAVIOR_MISMODEL','目标行为误建模','任务建模失败','S1'),
    ('C01_WRONG_CODE_LOCUS','模块或文件落点错误','上下文落点漂移','S2'),
    ('C02_WRONG_SYMBOL_OR_API_GENERATION','符号或API代际错位','上下文落点漂移','S2'),
    ('C03_WRONG_TEST_CONTAINER','测试容器落点错误','上下文落点漂移','S2'),
    ('P01_NON_DIAGNOSTIC_ORACLE','非诊断性断言','伪复现产物','S3'),
    ('I01_MOCK_MODEL_FAILURE','Mock建模失败','构造迭代失败','S3'),
    ('I02_FIXTURE_SETUP_FAILURE','Fixture或前置状态失败','构造迭代失败','S3'),
    ('I03_ASSERTION_ORACLE_MISMATCH','断言预期不匹配','构造迭代失败','S3'),
    ('I04_TEST_EXECUTION_ENTRY_FAILURE','测试执行入口失败','构造迭代失败','S3'),
    ('I05_FEEDBACK_NON_CONVERGENCE','反馈迭代未收敛','构造迭代失败','S3'),
    ('E01_F2P_COVERAGE_INCOMPLETE','有效F2P覆盖不足','评测契约对齐失败','S3'),
    ('E02_NEW_REGRESSION_P2F','新增回归P2F','评测契约对齐失败','S3'),
    ('E03_RESIDUAL_F2F','残留双版本失败F2F','评测契约对齐失败','S3'),
    ('A01_FIXED_VERSION_UNCHECKED','未检查修复版本即验收','过早验收失败','S4'),
]
TAXONOMY=[dict(code=c,name_zh=n,parent_mode=p,stage=s) for c,n,p,s in _MODES]
