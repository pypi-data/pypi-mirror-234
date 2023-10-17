# Generated from XQueryParser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .XQueryParser import XQueryParser
else:
    from XQueryParser import XQueryParser

# This class defines a complete listener for a parse tree produced by XQueryParser.
class XQueryParserListener(ParseTreeListener):

    # Enter a parse tree produced by XQueryParser#module.
    def enterModule(self, ctx:XQueryParser.ModuleContext):
        pass

    # Exit a parse tree produced by XQueryParser#module.
    def exitModule(self, ctx:XQueryParser.ModuleContext):
        pass


    # Enter a parse tree produced by XQueryParser#xqDocComment.
    def enterXqDocComment(self, ctx:XQueryParser.XqDocCommentContext):
        pass

    # Exit a parse tree produced by XQueryParser#xqDocComment.
    def exitXqDocComment(self, ctx:XQueryParser.XqDocCommentContext):
        pass


    # Enter a parse tree produced by XQueryParser#versionDecl.
    def enterVersionDecl(self, ctx:XQueryParser.VersionDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#versionDecl.
    def exitVersionDecl(self, ctx:XQueryParser.VersionDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#mainModule.
    def enterMainModule(self, ctx:XQueryParser.MainModuleContext):
        pass

    # Exit a parse tree produced by XQueryParser#mainModule.
    def exitMainModule(self, ctx:XQueryParser.MainModuleContext):
        pass


    # Enter a parse tree produced by XQueryParser#queryBody.
    def enterQueryBody(self, ctx:XQueryParser.QueryBodyContext):
        pass

    # Exit a parse tree produced by XQueryParser#queryBody.
    def exitQueryBody(self, ctx:XQueryParser.QueryBodyContext):
        pass


    # Enter a parse tree produced by XQueryParser#libraryModule.
    def enterLibraryModule(self, ctx:XQueryParser.LibraryModuleContext):
        pass

    # Exit a parse tree produced by XQueryParser#libraryModule.
    def exitLibraryModule(self, ctx:XQueryParser.LibraryModuleContext):
        pass


    # Enter a parse tree produced by XQueryParser#moduleDecl.
    def enterModuleDecl(self, ctx:XQueryParser.ModuleDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#moduleDecl.
    def exitModuleDecl(self, ctx:XQueryParser.ModuleDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#prolog.
    def enterProlog(self, ctx:XQueryParser.PrologContext):
        pass

    # Exit a parse tree produced by XQueryParser#prolog.
    def exitProlog(self, ctx:XQueryParser.PrologContext):
        pass


    # Enter a parse tree produced by XQueryParser#defaultNamespaceDecl.
    def enterDefaultNamespaceDecl(self, ctx:XQueryParser.DefaultNamespaceDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#defaultNamespaceDecl.
    def exitDefaultNamespaceDecl(self, ctx:XQueryParser.DefaultNamespaceDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#setter.
    def enterSetter(self, ctx:XQueryParser.SetterContext):
        pass

    # Exit a parse tree produced by XQueryParser#setter.
    def exitSetter(self, ctx:XQueryParser.SetterContext):
        pass


    # Enter a parse tree produced by XQueryParser#boundarySpaceDecl.
    def enterBoundarySpaceDecl(self, ctx:XQueryParser.BoundarySpaceDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#boundarySpaceDecl.
    def exitBoundarySpaceDecl(self, ctx:XQueryParser.BoundarySpaceDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#defaultCollationDecl.
    def enterDefaultCollationDecl(self, ctx:XQueryParser.DefaultCollationDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#defaultCollationDecl.
    def exitDefaultCollationDecl(self, ctx:XQueryParser.DefaultCollationDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#baseURIDecl.
    def enterBaseURIDecl(self, ctx:XQueryParser.BaseURIDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#baseURIDecl.
    def exitBaseURIDecl(self, ctx:XQueryParser.BaseURIDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#constructionDecl.
    def enterConstructionDecl(self, ctx:XQueryParser.ConstructionDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#constructionDecl.
    def exitConstructionDecl(self, ctx:XQueryParser.ConstructionDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#orderingModeDecl.
    def enterOrderingModeDecl(self, ctx:XQueryParser.OrderingModeDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#orderingModeDecl.
    def exitOrderingModeDecl(self, ctx:XQueryParser.OrderingModeDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#emptyOrderDecl.
    def enterEmptyOrderDecl(self, ctx:XQueryParser.EmptyOrderDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#emptyOrderDecl.
    def exitEmptyOrderDecl(self, ctx:XQueryParser.EmptyOrderDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#copyNamespacesDecl.
    def enterCopyNamespacesDecl(self, ctx:XQueryParser.CopyNamespacesDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#copyNamespacesDecl.
    def exitCopyNamespacesDecl(self, ctx:XQueryParser.CopyNamespacesDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#preserveMode.
    def enterPreserveMode(self, ctx:XQueryParser.PreserveModeContext):
        pass

    # Exit a parse tree produced by XQueryParser#preserveMode.
    def exitPreserveMode(self, ctx:XQueryParser.PreserveModeContext):
        pass


    # Enter a parse tree produced by XQueryParser#inheritMode.
    def enterInheritMode(self, ctx:XQueryParser.InheritModeContext):
        pass

    # Exit a parse tree produced by XQueryParser#inheritMode.
    def exitInheritMode(self, ctx:XQueryParser.InheritModeContext):
        pass


    # Enter a parse tree produced by XQueryParser#decimalFormatDecl.
    def enterDecimalFormatDecl(self, ctx:XQueryParser.DecimalFormatDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#decimalFormatDecl.
    def exitDecimalFormatDecl(self, ctx:XQueryParser.DecimalFormatDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#schemaImport.
    def enterSchemaImport(self, ctx:XQueryParser.SchemaImportContext):
        pass

    # Exit a parse tree produced by XQueryParser#schemaImport.
    def exitSchemaImport(self, ctx:XQueryParser.SchemaImportContext):
        pass


    # Enter a parse tree produced by XQueryParser#schemaPrefix.
    def enterSchemaPrefix(self, ctx:XQueryParser.SchemaPrefixContext):
        pass

    # Exit a parse tree produced by XQueryParser#schemaPrefix.
    def exitSchemaPrefix(self, ctx:XQueryParser.SchemaPrefixContext):
        pass


    # Enter a parse tree produced by XQueryParser#moduleImport.
    def enterModuleImport(self, ctx:XQueryParser.ModuleImportContext):
        pass

    # Exit a parse tree produced by XQueryParser#moduleImport.
    def exitModuleImport(self, ctx:XQueryParser.ModuleImportContext):
        pass


    # Enter a parse tree produced by XQueryParser#namespaceDecl.
    def enterNamespaceDecl(self, ctx:XQueryParser.NamespaceDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#namespaceDecl.
    def exitNamespaceDecl(self, ctx:XQueryParser.NamespaceDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#varDecl.
    def enterVarDecl(self, ctx:XQueryParser.VarDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#varDecl.
    def exitVarDecl(self, ctx:XQueryParser.VarDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#varValue.
    def enterVarValue(self, ctx:XQueryParser.VarValueContext):
        pass

    # Exit a parse tree produced by XQueryParser#varValue.
    def exitVarValue(self, ctx:XQueryParser.VarValueContext):
        pass


    # Enter a parse tree produced by XQueryParser#varDefaultValue.
    def enterVarDefaultValue(self, ctx:XQueryParser.VarDefaultValueContext):
        pass

    # Exit a parse tree produced by XQueryParser#varDefaultValue.
    def exitVarDefaultValue(self, ctx:XQueryParser.VarDefaultValueContext):
        pass


    # Enter a parse tree produced by XQueryParser#contextItemDecl.
    def enterContextItemDecl(self, ctx:XQueryParser.ContextItemDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#contextItemDecl.
    def exitContextItemDecl(self, ctx:XQueryParser.ContextItemDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionDecl.
    def enterFunctionDecl(self, ctx:XQueryParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionDecl.
    def exitFunctionDecl(self, ctx:XQueryParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionParams.
    def enterFunctionParams(self, ctx:XQueryParser.FunctionParamsContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionParams.
    def exitFunctionParams(self, ctx:XQueryParser.FunctionParamsContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionParam.
    def enterFunctionParam(self, ctx:XQueryParser.FunctionParamContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionParam.
    def exitFunctionParam(self, ctx:XQueryParser.FunctionParamContext):
        pass


    # Enter a parse tree produced by XQueryParser#annotations.
    def enterAnnotations(self, ctx:XQueryParser.AnnotationsContext):
        pass

    # Exit a parse tree produced by XQueryParser#annotations.
    def exitAnnotations(self, ctx:XQueryParser.AnnotationsContext):
        pass


    # Enter a parse tree produced by XQueryParser#annotation.
    def enterAnnotation(self, ctx:XQueryParser.AnnotationContext):
        pass

    # Exit a parse tree produced by XQueryParser#annotation.
    def exitAnnotation(self, ctx:XQueryParser.AnnotationContext):
        pass


    # Enter a parse tree produced by XQueryParser#annotList.
    def enterAnnotList(self, ctx:XQueryParser.AnnotListContext):
        pass

    # Exit a parse tree produced by XQueryParser#annotList.
    def exitAnnotList(self, ctx:XQueryParser.AnnotListContext):
        pass


    # Enter a parse tree produced by XQueryParser#annotationParam.
    def enterAnnotationParam(self, ctx:XQueryParser.AnnotationParamContext):
        pass

    # Exit a parse tree produced by XQueryParser#annotationParam.
    def exitAnnotationParam(self, ctx:XQueryParser.AnnotationParamContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionReturn.
    def enterFunctionReturn(self, ctx:XQueryParser.FunctionReturnContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionReturn.
    def exitFunctionReturn(self, ctx:XQueryParser.FunctionReturnContext):
        pass


    # Enter a parse tree produced by XQueryParser#optionDecl.
    def enterOptionDecl(self, ctx:XQueryParser.OptionDeclContext):
        pass

    # Exit a parse tree produced by XQueryParser#optionDecl.
    def exitOptionDecl(self, ctx:XQueryParser.OptionDeclContext):
        pass


    # Enter a parse tree produced by XQueryParser#expr.
    def enterExpr(self, ctx:XQueryParser.ExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#expr.
    def exitExpr(self, ctx:XQueryParser.ExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#exprSingle.
    def enterExprSingle(self, ctx:XQueryParser.ExprSingleContext):
        pass

    # Exit a parse tree produced by XQueryParser#exprSingle.
    def exitExprSingle(self, ctx:XQueryParser.ExprSingleContext):
        pass


    # Enter a parse tree produced by XQueryParser#flworExpr.
    def enterFlworExpr(self, ctx:XQueryParser.FlworExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#flworExpr.
    def exitFlworExpr(self, ctx:XQueryParser.FlworExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#initialClause.
    def enterInitialClause(self, ctx:XQueryParser.InitialClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#initialClause.
    def exitInitialClause(self, ctx:XQueryParser.InitialClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#intermediateClause.
    def enterIntermediateClause(self, ctx:XQueryParser.IntermediateClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#intermediateClause.
    def exitIntermediateClause(self, ctx:XQueryParser.IntermediateClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#forClause.
    def enterForClause(self, ctx:XQueryParser.ForClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#forClause.
    def exitForClause(self, ctx:XQueryParser.ForClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#forBinding.
    def enterForBinding(self, ctx:XQueryParser.ForBindingContext):
        pass

    # Exit a parse tree produced by XQueryParser#forBinding.
    def exitForBinding(self, ctx:XQueryParser.ForBindingContext):
        pass


    # Enter a parse tree produced by XQueryParser#allowingEmpty.
    def enterAllowingEmpty(self, ctx:XQueryParser.AllowingEmptyContext):
        pass

    # Exit a parse tree produced by XQueryParser#allowingEmpty.
    def exitAllowingEmpty(self, ctx:XQueryParser.AllowingEmptyContext):
        pass


    # Enter a parse tree produced by XQueryParser#positionalVar.
    def enterPositionalVar(self, ctx:XQueryParser.PositionalVarContext):
        pass

    # Exit a parse tree produced by XQueryParser#positionalVar.
    def exitPositionalVar(self, ctx:XQueryParser.PositionalVarContext):
        pass


    # Enter a parse tree produced by XQueryParser#letClause.
    def enterLetClause(self, ctx:XQueryParser.LetClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#letClause.
    def exitLetClause(self, ctx:XQueryParser.LetClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#letBinding.
    def enterLetBinding(self, ctx:XQueryParser.LetBindingContext):
        pass

    # Exit a parse tree produced by XQueryParser#letBinding.
    def exitLetBinding(self, ctx:XQueryParser.LetBindingContext):
        pass


    # Enter a parse tree produced by XQueryParser#windowClause.
    def enterWindowClause(self, ctx:XQueryParser.WindowClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#windowClause.
    def exitWindowClause(self, ctx:XQueryParser.WindowClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#tumblingWindowClause.
    def enterTumblingWindowClause(self, ctx:XQueryParser.TumblingWindowClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#tumblingWindowClause.
    def exitTumblingWindowClause(self, ctx:XQueryParser.TumblingWindowClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#slidingWindowClause.
    def enterSlidingWindowClause(self, ctx:XQueryParser.SlidingWindowClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#slidingWindowClause.
    def exitSlidingWindowClause(self, ctx:XQueryParser.SlidingWindowClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#windowStartCondition.
    def enterWindowStartCondition(self, ctx:XQueryParser.WindowStartConditionContext):
        pass

    # Exit a parse tree produced by XQueryParser#windowStartCondition.
    def exitWindowStartCondition(self, ctx:XQueryParser.WindowStartConditionContext):
        pass


    # Enter a parse tree produced by XQueryParser#windowEndCondition.
    def enterWindowEndCondition(self, ctx:XQueryParser.WindowEndConditionContext):
        pass

    # Exit a parse tree produced by XQueryParser#windowEndCondition.
    def exitWindowEndCondition(self, ctx:XQueryParser.WindowEndConditionContext):
        pass


    # Enter a parse tree produced by XQueryParser#windowVars.
    def enterWindowVars(self, ctx:XQueryParser.WindowVarsContext):
        pass

    # Exit a parse tree produced by XQueryParser#windowVars.
    def exitWindowVars(self, ctx:XQueryParser.WindowVarsContext):
        pass


    # Enter a parse tree produced by XQueryParser#countClause.
    def enterCountClause(self, ctx:XQueryParser.CountClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#countClause.
    def exitCountClause(self, ctx:XQueryParser.CountClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#whereClause.
    def enterWhereClause(self, ctx:XQueryParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#whereClause.
    def exitWhereClause(self, ctx:XQueryParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#groupByClause.
    def enterGroupByClause(self, ctx:XQueryParser.GroupByClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#groupByClause.
    def exitGroupByClause(self, ctx:XQueryParser.GroupByClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#groupingSpecList.
    def enterGroupingSpecList(self, ctx:XQueryParser.GroupingSpecListContext):
        pass

    # Exit a parse tree produced by XQueryParser#groupingSpecList.
    def exitGroupingSpecList(self, ctx:XQueryParser.GroupingSpecListContext):
        pass


    # Enter a parse tree produced by XQueryParser#groupingSpec.
    def enterGroupingSpec(self, ctx:XQueryParser.GroupingSpecContext):
        pass

    # Exit a parse tree produced by XQueryParser#groupingSpec.
    def exitGroupingSpec(self, ctx:XQueryParser.GroupingSpecContext):
        pass


    # Enter a parse tree produced by XQueryParser#orderByClause.
    def enterOrderByClause(self, ctx:XQueryParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#orderByClause.
    def exitOrderByClause(self, ctx:XQueryParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#orderSpec.
    def enterOrderSpec(self, ctx:XQueryParser.OrderSpecContext):
        pass

    # Exit a parse tree produced by XQueryParser#orderSpec.
    def exitOrderSpec(self, ctx:XQueryParser.OrderSpecContext):
        pass


    # Enter a parse tree produced by XQueryParser#returnClause.
    def enterReturnClause(self, ctx:XQueryParser.ReturnClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#returnClause.
    def exitReturnClause(self, ctx:XQueryParser.ReturnClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#quantifiedExpr.
    def enterQuantifiedExpr(self, ctx:XQueryParser.QuantifiedExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#quantifiedExpr.
    def exitQuantifiedExpr(self, ctx:XQueryParser.QuantifiedExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#quantifiedVar.
    def enterQuantifiedVar(self, ctx:XQueryParser.QuantifiedVarContext):
        pass

    # Exit a parse tree produced by XQueryParser#quantifiedVar.
    def exitQuantifiedVar(self, ctx:XQueryParser.QuantifiedVarContext):
        pass


    # Enter a parse tree produced by XQueryParser#switchExpr.
    def enterSwitchExpr(self, ctx:XQueryParser.SwitchExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#switchExpr.
    def exitSwitchExpr(self, ctx:XQueryParser.SwitchExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#switchCaseClause.
    def enterSwitchCaseClause(self, ctx:XQueryParser.SwitchCaseClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#switchCaseClause.
    def exitSwitchCaseClause(self, ctx:XQueryParser.SwitchCaseClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#switchCaseOperand.
    def enterSwitchCaseOperand(self, ctx:XQueryParser.SwitchCaseOperandContext):
        pass

    # Exit a parse tree produced by XQueryParser#switchCaseOperand.
    def exitSwitchCaseOperand(self, ctx:XQueryParser.SwitchCaseOperandContext):
        pass


    # Enter a parse tree produced by XQueryParser#typeswitchExpr.
    def enterTypeswitchExpr(self, ctx:XQueryParser.TypeswitchExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#typeswitchExpr.
    def exitTypeswitchExpr(self, ctx:XQueryParser.TypeswitchExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#caseClause.
    def enterCaseClause(self, ctx:XQueryParser.CaseClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#caseClause.
    def exitCaseClause(self, ctx:XQueryParser.CaseClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#sequenceUnionType.
    def enterSequenceUnionType(self, ctx:XQueryParser.SequenceUnionTypeContext):
        pass

    # Exit a parse tree produced by XQueryParser#sequenceUnionType.
    def exitSequenceUnionType(self, ctx:XQueryParser.SequenceUnionTypeContext):
        pass


    # Enter a parse tree produced by XQueryParser#ifExpr.
    def enterIfExpr(self, ctx:XQueryParser.IfExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#ifExpr.
    def exitIfExpr(self, ctx:XQueryParser.IfExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#tryCatchExpr.
    def enterTryCatchExpr(self, ctx:XQueryParser.TryCatchExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#tryCatchExpr.
    def exitTryCatchExpr(self, ctx:XQueryParser.TryCatchExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#tryClause.
    def enterTryClause(self, ctx:XQueryParser.TryClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#tryClause.
    def exitTryClause(self, ctx:XQueryParser.TryClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#enclosedTryTargetExpression.
    def enterEnclosedTryTargetExpression(self, ctx:XQueryParser.EnclosedTryTargetExpressionContext):
        pass

    # Exit a parse tree produced by XQueryParser#enclosedTryTargetExpression.
    def exitEnclosedTryTargetExpression(self, ctx:XQueryParser.EnclosedTryTargetExpressionContext):
        pass


    # Enter a parse tree produced by XQueryParser#catchClause.
    def enterCatchClause(self, ctx:XQueryParser.CatchClauseContext):
        pass

    # Exit a parse tree produced by XQueryParser#catchClause.
    def exitCatchClause(self, ctx:XQueryParser.CatchClauseContext):
        pass


    # Enter a parse tree produced by XQueryParser#enclosedExpression.
    def enterEnclosedExpression(self, ctx:XQueryParser.EnclosedExpressionContext):
        pass

    # Exit a parse tree produced by XQueryParser#enclosedExpression.
    def exitEnclosedExpression(self, ctx:XQueryParser.EnclosedExpressionContext):
        pass


    # Enter a parse tree produced by XQueryParser#catchErrorList.
    def enterCatchErrorList(self, ctx:XQueryParser.CatchErrorListContext):
        pass

    # Exit a parse tree produced by XQueryParser#catchErrorList.
    def exitCatchErrorList(self, ctx:XQueryParser.CatchErrorListContext):
        pass


    # Enter a parse tree produced by XQueryParser#existUpdateExpr.
    def enterExistUpdateExpr(self, ctx:XQueryParser.ExistUpdateExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#existUpdateExpr.
    def exitExistUpdateExpr(self, ctx:XQueryParser.ExistUpdateExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#existReplaceExpr.
    def enterExistReplaceExpr(self, ctx:XQueryParser.ExistReplaceExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#existReplaceExpr.
    def exitExistReplaceExpr(self, ctx:XQueryParser.ExistReplaceExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#existValueExpr.
    def enterExistValueExpr(self, ctx:XQueryParser.ExistValueExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#existValueExpr.
    def exitExistValueExpr(self, ctx:XQueryParser.ExistValueExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#existInsertExpr.
    def enterExistInsertExpr(self, ctx:XQueryParser.ExistInsertExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#existInsertExpr.
    def exitExistInsertExpr(self, ctx:XQueryParser.ExistInsertExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#existDeleteExpr.
    def enterExistDeleteExpr(self, ctx:XQueryParser.ExistDeleteExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#existDeleteExpr.
    def exitExistDeleteExpr(self, ctx:XQueryParser.ExistDeleteExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#existRenameExpr.
    def enterExistRenameExpr(self, ctx:XQueryParser.ExistRenameExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#existRenameExpr.
    def exitExistRenameExpr(self, ctx:XQueryParser.ExistRenameExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#orExpr.
    def enterOrExpr(self, ctx:XQueryParser.OrExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#orExpr.
    def exitOrExpr(self, ctx:XQueryParser.OrExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#andExpr.
    def enterAndExpr(self, ctx:XQueryParser.AndExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#andExpr.
    def exitAndExpr(self, ctx:XQueryParser.AndExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#comparisonExpr.
    def enterComparisonExpr(self, ctx:XQueryParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#comparisonExpr.
    def exitComparisonExpr(self, ctx:XQueryParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringConcatExpr.
    def enterStringConcatExpr(self, ctx:XQueryParser.StringConcatExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringConcatExpr.
    def exitStringConcatExpr(self, ctx:XQueryParser.StringConcatExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#rangeExpr.
    def enterRangeExpr(self, ctx:XQueryParser.RangeExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#rangeExpr.
    def exitRangeExpr(self, ctx:XQueryParser.RangeExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:XQueryParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:XQueryParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:XQueryParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:XQueryParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#unionExpr.
    def enterUnionExpr(self, ctx:XQueryParser.UnionExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#unionExpr.
    def exitUnionExpr(self, ctx:XQueryParser.UnionExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#intersectExceptExpr.
    def enterIntersectExceptExpr(self, ctx:XQueryParser.IntersectExceptExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#intersectExceptExpr.
    def exitIntersectExceptExpr(self, ctx:XQueryParser.IntersectExceptExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#instanceOfExpr.
    def enterInstanceOfExpr(self, ctx:XQueryParser.InstanceOfExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#instanceOfExpr.
    def exitInstanceOfExpr(self, ctx:XQueryParser.InstanceOfExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#treatExpr.
    def enterTreatExpr(self, ctx:XQueryParser.TreatExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#treatExpr.
    def exitTreatExpr(self, ctx:XQueryParser.TreatExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#castableExpr.
    def enterCastableExpr(self, ctx:XQueryParser.CastableExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#castableExpr.
    def exitCastableExpr(self, ctx:XQueryParser.CastableExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#castExpr.
    def enterCastExpr(self, ctx:XQueryParser.CastExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#castExpr.
    def exitCastExpr(self, ctx:XQueryParser.CastExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#arrowExpr.
    def enterArrowExpr(self, ctx:XQueryParser.ArrowExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#arrowExpr.
    def exitArrowExpr(self, ctx:XQueryParser.ArrowExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#unaryExpression.
    def enterUnaryExpression(self, ctx:XQueryParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by XQueryParser#unaryExpression.
    def exitUnaryExpression(self, ctx:XQueryParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by XQueryParser#valueExpr.
    def enterValueExpr(self, ctx:XQueryParser.ValueExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#valueExpr.
    def exitValueExpr(self, ctx:XQueryParser.ValueExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#generalComp.
    def enterGeneralComp(self, ctx:XQueryParser.GeneralCompContext):
        pass

    # Exit a parse tree produced by XQueryParser#generalComp.
    def exitGeneralComp(self, ctx:XQueryParser.GeneralCompContext):
        pass


    # Enter a parse tree produced by XQueryParser#valueComp.
    def enterValueComp(self, ctx:XQueryParser.ValueCompContext):
        pass

    # Exit a parse tree produced by XQueryParser#valueComp.
    def exitValueComp(self, ctx:XQueryParser.ValueCompContext):
        pass


    # Enter a parse tree produced by XQueryParser#nodeComp.
    def enterNodeComp(self, ctx:XQueryParser.NodeCompContext):
        pass

    # Exit a parse tree produced by XQueryParser#nodeComp.
    def exitNodeComp(self, ctx:XQueryParser.NodeCompContext):
        pass


    # Enter a parse tree produced by XQueryParser#validateExpr.
    def enterValidateExpr(self, ctx:XQueryParser.ValidateExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#validateExpr.
    def exitValidateExpr(self, ctx:XQueryParser.ValidateExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#validationMode.
    def enterValidationMode(self, ctx:XQueryParser.ValidationModeContext):
        pass

    # Exit a parse tree produced by XQueryParser#validationMode.
    def exitValidationMode(self, ctx:XQueryParser.ValidationModeContext):
        pass


    # Enter a parse tree produced by XQueryParser#extensionExpr.
    def enterExtensionExpr(self, ctx:XQueryParser.ExtensionExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#extensionExpr.
    def exitExtensionExpr(self, ctx:XQueryParser.ExtensionExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#simpleMapExpr.
    def enterSimpleMapExpr(self, ctx:XQueryParser.SimpleMapExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#simpleMapExpr.
    def exitSimpleMapExpr(self, ctx:XQueryParser.SimpleMapExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#pathExpr.
    def enterPathExpr(self, ctx:XQueryParser.PathExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#pathExpr.
    def exitPathExpr(self, ctx:XQueryParser.PathExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#relativePathExpr.
    def enterRelativePathExpr(self, ctx:XQueryParser.RelativePathExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#relativePathExpr.
    def exitRelativePathExpr(self, ctx:XQueryParser.RelativePathExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#stepExpr.
    def enterStepExpr(self, ctx:XQueryParser.StepExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#stepExpr.
    def exitStepExpr(self, ctx:XQueryParser.StepExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#axisStep.
    def enterAxisStep(self, ctx:XQueryParser.AxisStepContext):
        pass

    # Exit a parse tree produced by XQueryParser#axisStep.
    def exitAxisStep(self, ctx:XQueryParser.AxisStepContext):
        pass


    # Enter a parse tree produced by XQueryParser#forwardStep.
    def enterForwardStep(self, ctx:XQueryParser.ForwardStepContext):
        pass

    # Exit a parse tree produced by XQueryParser#forwardStep.
    def exitForwardStep(self, ctx:XQueryParser.ForwardStepContext):
        pass


    # Enter a parse tree produced by XQueryParser#forwardAxis.
    def enterForwardAxis(self, ctx:XQueryParser.ForwardAxisContext):
        pass

    # Exit a parse tree produced by XQueryParser#forwardAxis.
    def exitForwardAxis(self, ctx:XQueryParser.ForwardAxisContext):
        pass


    # Enter a parse tree produced by XQueryParser#abbrevForwardStep.
    def enterAbbrevForwardStep(self, ctx:XQueryParser.AbbrevForwardStepContext):
        pass

    # Exit a parse tree produced by XQueryParser#abbrevForwardStep.
    def exitAbbrevForwardStep(self, ctx:XQueryParser.AbbrevForwardStepContext):
        pass


    # Enter a parse tree produced by XQueryParser#reverseStep.
    def enterReverseStep(self, ctx:XQueryParser.ReverseStepContext):
        pass

    # Exit a parse tree produced by XQueryParser#reverseStep.
    def exitReverseStep(self, ctx:XQueryParser.ReverseStepContext):
        pass


    # Enter a parse tree produced by XQueryParser#reverseAxis.
    def enterReverseAxis(self, ctx:XQueryParser.ReverseAxisContext):
        pass

    # Exit a parse tree produced by XQueryParser#reverseAxis.
    def exitReverseAxis(self, ctx:XQueryParser.ReverseAxisContext):
        pass


    # Enter a parse tree produced by XQueryParser#abbrevReverseStep.
    def enterAbbrevReverseStep(self, ctx:XQueryParser.AbbrevReverseStepContext):
        pass

    # Exit a parse tree produced by XQueryParser#abbrevReverseStep.
    def exitAbbrevReverseStep(self, ctx:XQueryParser.AbbrevReverseStepContext):
        pass


    # Enter a parse tree produced by XQueryParser#nodeTest.
    def enterNodeTest(self, ctx:XQueryParser.NodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#nodeTest.
    def exitNodeTest(self, ctx:XQueryParser.NodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#nameTest.
    def enterNameTest(self, ctx:XQueryParser.NameTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#nameTest.
    def exitNameTest(self, ctx:XQueryParser.NameTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#allNames.
    def enterAllNames(self, ctx:XQueryParser.AllNamesContext):
        pass

    # Exit a parse tree produced by XQueryParser#allNames.
    def exitAllNames(self, ctx:XQueryParser.AllNamesContext):
        pass


    # Enter a parse tree produced by XQueryParser#allWithNS.
    def enterAllWithNS(self, ctx:XQueryParser.AllWithNSContext):
        pass

    # Exit a parse tree produced by XQueryParser#allWithNS.
    def exitAllWithNS(self, ctx:XQueryParser.AllWithNSContext):
        pass


    # Enter a parse tree produced by XQueryParser#allWithLocal.
    def enterAllWithLocal(self, ctx:XQueryParser.AllWithLocalContext):
        pass

    # Exit a parse tree produced by XQueryParser#allWithLocal.
    def exitAllWithLocal(self, ctx:XQueryParser.AllWithLocalContext):
        pass


    # Enter a parse tree produced by XQueryParser#postfixExpr.
    def enterPostfixExpr(self, ctx:XQueryParser.PostfixExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#postfixExpr.
    def exitPostfixExpr(self, ctx:XQueryParser.PostfixExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#argumentList.
    def enterArgumentList(self, ctx:XQueryParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by XQueryParser#argumentList.
    def exitArgumentList(self, ctx:XQueryParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by XQueryParser#predicateList.
    def enterPredicateList(self, ctx:XQueryParser.PredicateListContext):
        pass

    # Exit a parse tree produced by XQueryParser#predicateList.
    def exitPredicateList(self, ctx:XQueryParser.PredicateListContext):
        pass


    # Enter a parse tree produced by XQueryParser#predicate.
    def enterPredicate(self, ctx:XQueryParser.PredicateContext):
        pass

    # Exit a parse tree produced by XQueryParser#predicate.
    def exitPredicate(self, ctx:XQueryParser.PredicateContext):
        pass


    # Enter a parse tree produced by XQueryParser#lookup.
    def enterLookup(self, ctx:XQueryParser.LookupContext):
        pass

    # Exit a parse tree produced by XQueryParser#lookup.
    def exitLookup(self, ctx:XQueryParser.LookupContext):
        pass


    # Enter a parse tree produced by XQueryParser#keySpecifier.
    def enterKeySpecifier(self, ctx:XQueryParser.KeySpecifierContext):
        pass

    # Exit a parse tree produced by XQueryParser#keySpecifier.
    def exitKeySpecifier(self, ctx:XQueryParser.KeySpecifierContext):
        pass


    # Enter a parse tree produced by XQueryParser#arrowFunctionSpecifier.
    def enterArrowFunctionSpecifier(self, ctx:XQueryParser.ArrowFunctionSpecifierContext):
        pass

    # Exit a parse tree produced by XQueryParser#arrowFunctionSpecifier.
    def exitArrowFunctionSpecifier(self, ctx:XQueryParser.ArrowFunctionSpecifierContext):
        pass


    # Enter a parse tree produced by XQueryParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:XQueryParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:XQueryParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#literal.
    def enterLiteral(self, ctx:XQueryParser.LiteralContext):
        pass

    # Exit a parse tree produced by XQueryParser#literal.
    def exitLiteral(self, ctx:XQueryParser.LiteralContext):
        pass


    # Enter a parse tree produced by XQueryParser#numericLiteral.
    def enterNumericLiteral(self, ctx:XQueryParser.NumericLiteralContext):
        pass

    # Exit a parse tree produced by XQueryParser#numericLiteral.
    def exitNumericLiteral(self, ctx:XQueryParser.NumericLiteralContext):
        pass


    # Enter a parse tree produced by XQueryParser#varRef.
    def enterVarRef(self, ctx:XQueryParser.VarRefContext):
        pass

    # Exit a parse tree produced by XQueryParser#varRef.
    def exitVarRef(self, ctx:XQueryParser.VarRefContext):
        pass


    # Enter a parse tree produced by XQueryParser#varName.
    def enterVarName(self, ctx:XQueryParser.VarNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#varName.
    def exitVarName(self, ctx:XQueryParser.VarNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#parenthesizedExpr.
    def enterParenthesizedExpr(self, ctx:XQueryParser.ParenthesizedExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#parenthesizedExpr.
    def exitParenthesizedExpr(self, ctx:XQueryParser.ParenthesizedExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#contextItemExpr.
    def enterContextItemExpr(self, ctx:XQueryParser.ContextItemExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#contextItemExpr.
    def exitContextItemExpr(self, ctx:XQueryParser.ContextItemExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#orderedExpr.
    def enterOrderedExpr(self, ctx:XQueryParser.OrderedExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#orderedExpr.
    def exitOrderedExpr(self, ctx:XQueryParser.OrderedExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#unorderedExpr.
    def enterUnorderedExpr(self, ctx:XQueryParser.UnorderedExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#unorderedExpr.
    def exitUnorderedExpr(self, ctx:XQueryParser.UnorderedExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionCall.
    def enterFunctionCall(self, ctx:XQueryParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionCall.
    def exitFunctionCall(self, ctx:XQueryParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by XQueryParser#argument.
    def enterArgument(self, ctx:XQueryParser.ArgumentContext):
        pass

    # Exit a parse tree produced by XQueryParser#argument.
    def exitArgument(self, ctx:XQueryParser.ArgumentContext):
        pass


    # Enter a parse tree produced by XQueryParser#nodeConstructor.
    def enterNodeConstructor(self, ctx:XQueryParser.NodeConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#nodeConstructor.
    def exitNodeConstructor(self, ctx:XQueryParser.NodeConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#directConstructor.
    def enterDirectConstructor(self, ctx:XQueryParser.DirectConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#directConstructor.
    def exitDirectConstructor(self, ctx:XQueryParser.DirectConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirElemConstructorOpenClose.
    def enterDirElemConstructorOpenClose(self, ctx:XQueryParser.DirElemConstructorOpenCloseContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirElemConstructorOpenClose.
    def exitDirElemConstructorOpenClose(self, ctx:XQueryParser.DirElemConstructorOpenCloseContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirElemConstructorSingleTag.
    def enterDirElemConstructorSingleTag(self, ctx:XQueryParser.DirElemConstructorSingleTagContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirElemConstructorSingleTag.
    def exitDirElemConstructorSingleTag(self, ctx:XQueryParser.DirElemConstructorSingleTagContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirAttributeList.
    def enterDirAttributeList(self, ctx:XQueryParser.DirAttributeListContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirAttributeList.
    def exitDirAttributeList(self, ctx:XQueryParser.DirAttributeListContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirAttributeValueApos.
    def enterDirAttributeValueApos(self, ctx:XQueryParser.DirAttributeValueAposContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirAttributeValueApos.
    def exitDirAttributeValueApos(self, ctx:XQueryParser.DirAttributeValueAposContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirAttributeValueQuot.
    def enterDirAttributeValueQuot(self, ctx:XQueryParser.DirAttributeValueQuotContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirAttributeValueQuot.
    def exitDirAttributeValueQuot(self, ctx:XQueryParser.DirAttributeValueQuotContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirAttributeValue.
    def enterDirAttributeValue(self, ctx:XQueryParser.DirAttributeValueContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirAttributeValue.
    def exitDirAttributeValue(self, ctx:XQueryParser.DirAttributeValueContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirAttributeContentQuot.
    def enterDirAttributeContentQuot(self, ctx:XQueryParser.DirAttributeContentQuotContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirAttributeContentQuot.
    def exitDirAttributeContentQuot(self, ctx:XQueryParser.DirAttributeContentQuotContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirAttributeContentApos.
    def enterDirAttributeContentApos(self, ctx:XQueryParser.DirAttributeContentAposContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirAttributeContentApos.
    def exitDirAttributeContentApos(self, ctx:XQueryParser.DirAttributeContentAposContext):
        pass


    # Enter a parse tree produced by XQueryParser#dirElemContent.
    def enterDirElemContent(self, ctx:XQueryParser.DirElemContentContext):
        pass

    # Exit a parse tree produced by XQueryParser#dirElemContent.
    def exitDirElemContent(self, ctx:XQueryParser.DirElemContentContext):
        pass


    # Enter a parse tree produced by XQueryParser#commonContent.
    def enterCommonContent(self, ctx:XQueryParser.CommonContentContext):
        pass

    # Exit a parse tree produced by XQueryParser#commonContent.
    def exitCommonContent(self, ctx:XQueryParser.CommonContentContext):
        pass


    # Enter a parse tree produced by XQueryParser#computedConstructor.
    def enterComputedConstructor(self, ctx:XQueryParser.ComputedConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#computedConstructor.
    def exitComputedConstructor(self, ctx:XQueryParser.ComputedConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compMLJSONConstructor.
    def enterCompMLJSONConstructor(self, ctx:XQueryParser.CompMLJSONConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compMLJSONConstructor.
    def exitCompMLJSONConstructor(self, ctx:XQueryParser.CompMLJSONConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compMLJSONArrayConstructor.
    def enterCompMLJSONArrayConstructor(self, ctx:XQueryParser.CompMLJSONArrayConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compMLJSONArrayConstructor.
    def exitCompMLJSONArrayConstructor(self, ctx:XQueryParser.CompMLJSONArrayConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compMLJSONObjectConstructor.
    def enterCompMLJSONObjectConstructor(self, ctx:XQueryParser.CompMLJSONObjectConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compMLJSONObjectConstructor.
    def exitCompMLJSONObjectConstructor(self, ctx:XQueryParser.CompMLJSONObjectConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compMLJSONNumberConstructor.
    def enterCompMLJSONNumberConstructor(self, ctx:XQueryParser.CompMLJSONNumberConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compMLJSONNumberConstructor.
    def exitCompMLJSONNumberConstructor(self, ctx:XQueryParser.CompMLJSONNumberConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compMLJSONBooleanConstructor.
    def enterCompMLJSONBooleanConstructor(self, ctx:XQueryParser.CompMLJSONBooleanConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compMLJSONBooleanConstructor.
    def exitCompMLJSONBooleanConstructor(self, ctx:XQueryParser.CompMLJSONBooleanConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compMLJSONNullConstructor.
    def enterCompMLJSONNullConstructor(self, ctx:XQueryParser.CompMLJSONNullConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compMLJSONNullConstructor.
    def exitCompMLJSONNullConstructor(self, ctx:XQueryParser.CompMLJSONNullConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compBinaryConstructor.
    def enterCompBinaryConstructor(self, ctx:XQueryParser.CompBinaryConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compBinaryConstructor.
    def exitCompBinaryConstructor(self, ctx:XQueryParser.CompBinaryConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compDocConstructor.
    def enterCompDocConstructor(self, ctx:XQueryParser.CompDocConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compDocConstructor.
    def exitCompDocConstructor(self, ctx:XQueryParser.CompDocConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compElemConstructor.
    def enterCompElemConstructor(self, ctx:XQueryParser.CompElemConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compElemConstructor.
    def exitCompElemConstructor(self, ctx:XQueryParser.CompElemConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#enclosedContentExpr.
    def enterEnclosedContentExpr(self, ctx:XQueryParser.EnclosedContentExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#enclosedContentExpr.
    def exitEnclosedContentExpr(self, ctx:XQueryParser.EnclosedContentExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#compAttrConstructor.
    def enterCompAttrConstructor(self, ctx:XQueryParser.CompAttrConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compAttrConstructor.
    def exitCompAttrConstructor(self, ctx:XQueryParser.CompAttrConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compNamespaceConstructor.
    def enterCompNamespaceConstructor(self, ctx:XQueryParser.CompNamespaceConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compNamespaceConstructor.
    def exitCompNamespaceConstructor(self, ctx:XQueryParser.CompNamespaceConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#prefix.
    def enterPrefix(self, ctx:XQueryParser.PrefixContext):
        pass

    # Exit a parse tree produced by XQueryParser#prefix.
    def exitPrefix(self, ctx:XQueryParser.PrefixContext):
        pass


    # Enter a parse tree produced by XQueryParser#enclosedPrefixExpr.
    def enterEnclosedPrefixExpr(self, ctx:XQueryParser.EnclosedPrefixExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#enclosedPrefixExpr.
    def exitEnclosedPrefixExpr(self, ctx:XQueryParser.EnclosedPrefixExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#enclosedURIExpr.
    def enterEnclosedURIExpr(self, ctx:XQueryParser.EnclosedURIExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#enclosedURIExpr.
    def exitEnclosedURIExpr(self, ctx:XQueryParser.EnclosedURIExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#compTextConstructor.
    def enterCompTextConstructor(self, ctx:XQueryParser.CompTextConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compTextConstructor.
    def exitCompTextConstructor(self, ctx:XQueryParser.CompTextConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compCommentConstructor.
    def enterCompCommentConstructor(self, ctx:XQueryParser.CompCommentConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compCommentConstructor.
    def exitCompCommentConstructor(self, ctx:XQueryParser.CompCommentConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#compPIConstructor.
    def enterCompPIConstructor(self, ctx:XQueryParser.CompPIConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#compPIConstructor.
    def exitCompPIConstructor(self, ctx:XQueryParser.CompPIConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionItemExpr.
    def enterFunctionItemExpr(self, ctx:XQueryParser.FunctionItemExprContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionItemExpr.
    def exitFunctionItemExpr(self, ctx:XQueryParser.FunctionItemExprContext):
        pass


    # Enter a parse tree produced by XQueryParser#namedFunctionRef.
    def enterNamedFunctionRef(self, ctx:XQueryParser.NamedFunctionRefContext):
        pass

    # Exit a parse tree produced by XQueryParser#namedFunctionRef.
    def exitNamedFunctionRef(self, ctx:XQueryParser.NamedFunctionRefContext):
        pass


    # Enter a parse tree produced by XQueryParser#inlineFunctionRef.
    def enterInlineFunctionRef(self, ctx:XQueryParser.InlineFunctionRefContext):
        pass

    # Exit a parse tree produced by XQueryParser#inlineFunctionRef.
    def exitInlineFunctionRef(self, ctx:XQueryParser.InlineFunctionRefContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionBody.
    def enterFunctionBody(self, ctx:XQueryParser.FunctionBodyContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionBody.
    def exitFunctionBody(self, ctx:XQueryParser.FunctionBodyContext):
        pass


    # Enter a parse tree produced by XQueryParser#mapConstructor.
    def enterMapConstructor(self, ctx:XQueryParser.MapConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#mapConstructor.
    def exitMapConstructor(self, ctx:XQueryParser.MapConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#mapConstructorEntry.
    def enterMapConstructorEntry(self, ctx:XQueryParser.MapConstructorEntryContext):
        pass

    # Exit a parse tree produced by XQueryParser#mapConstructorEntry.
    def exitMapConstructorEntry(self, ctx:XQueryParser.MapConstructorEntryContext):
        pass


    # Enter a parse tree produced by XQueryParser#arrayConstructor.
    def enterArrayConstructor(self, ctx:XQueryParser.ArrayConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#arrayConstructor.
    def exitArrayConstructor(self, ctx:XQueryParser.ArrayConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#squareArrayConstructor.
    def enterSquareArrayConstructor(self, ctx:XQueryParser.SquareArrayConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#squareArrayConstructor.
    def exitSquareArrayConstructor(self, ctx:XQueryParser.SquareArrayConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#curlyArrayConstructor.
    def enterCurlyArrayConstructor(self, ctx:XQueryParser.CurlyArrayConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#curlyArrayConstructor.
    def exitCurlyArrayConstructor(self, ctx:XQueryParser.CurlyArrayConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringConstructor.
    def enterStringConstructor(self, ctx:XQueryParser.StringConstructorContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringConstructor.
    def exitStringConstructor(self, ctx:XQueryParser.StringConstructorContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringConstructorContent.
    def enterStringConstructorContent(self, ctx:XQueryParser.StringConstructorContentContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringConstructorContent.
    def exitStringConstructorContent(self, ctx:XQueryParser.StringConstructorContentContext):
        pass


    # Enter a parse tree produced by XQueryParser#charNoGrave.
    def enterCharNoGrave(self, ctx:XQueryParser.CharNoGraveContext):
        pass

    # Exit a parse tree produced by XQueryParser#charNoGrave.
    def exitCharNoGrave(self, ctx:XQueryParser.CharNoGraveContext):
        pass


    # Enter a parse tree produced by XQueryParser#charNoLBrace.
    def enterCharNoLBrace(self, ctx:XQueryParser.CharNoLBraceContext):
        pass

    # Exit a parse tree produced by XQueryParser#charNoLBrace.
    def exitCharNoLBrace(self, ctx:XQueryParser.CharNoLBraceContext):
        pass


    # Enter a parse tree produced by XQueryParser#charNoRBrack.
    def enterCharNoRBrack(self, ctx:XQueryParser.CharNoRBrackContext):
        pass

    # Exit a parse tree produced by XQueryParser#charNoRBrack.
    def exitCharNoRBrack(self, ctx:XQueryParser.CharNoRBrackContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringConstructorChars.
    def enterStringConstructorChars(self, ctx:XQueryParser.StringConstructorCharsContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringConstructorChars.
    def exitStringConstructorChars(self, ctx:XQueryParser.StringConstructorCharsContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringConstructorInterpolation.
    def enterStringConstructorInterpolation(self, ctx:XQueryParser.StringConstructorInterpolationContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringConstructorInterpolation.
    def exitStringConstructorInterpolation(self, ctx:XQueryParser.StringConstructorInterpolationContext):
        pass


    # Enter a parse tree produced by XQueryParser#unaryLookup.
    def enterUnaryLookup(self, ctx:XQueryParser.UnaryLookupContext):
        pass

    # Exit a parse tree produced by XQueryParser#unaryLookup.
    def exitUnaryLookup(self, ctx:XQueryParser.UnaryLookupContext):
        pass


    # Enter a parse tree produced by XQueryParser#singleType.
    def enterSingleType(self, ctx:XQueryParser.SingleTypeContext):
        pass

    # Exit a parse tree produced by XQueryParser#singleType.
    def exitSingleType(self, ctx:XQueryParser.SingleTypeContext):
        pass


    # Enter a parse tree produced by XQueryParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:XQueryParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by XQueryParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:XQueryParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by XQueryParser#sequenceType.
    def enterSequenceType(self, ctx:XQueryParser.SequenceTypeContext):
        pass

    # Exit a parse tree produced by XQueryParser#sequenceType.
    def exitSequenceType(self, ctx:XQueryParser.SequenceTypeContext):
        pass


    # Enter a parse tree produced by XQueryParser#itemType.
    def enterItemType(self, ctx:XQueryParser.ItemTypeContext):
        pass

    # Exit a parse tree produced by XQueryParser#itemType.
    def exitItemType(self, ctx:XQueryParser.ItemTypeContext):
        pass


    # Enter a parse tree produced by XQueryParser#atomicOrUnionType.
    def enterAtomicOrUnionType(self, ctx:XQueryParser.AtomicOrUnionTypeContext):
        pass

    # Exit a parse tree produced by XQueryParser#atomicOrUnionType.
    def exitAtomicOrUnionType(self, ctx:XQueryParser.AtomicOrUnionTypeContext):
        pass


    # Enter a parse tree produced by XQueryParser#kindTest.
    def enterKindTest(self, ctx:XQueryParser.KindTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#kindTest.
    def exitKindTest(self, ctx:XQueryParser.KindTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#anyKindTest.
    def enterAnyKindTest(self, ctx:XQueryParser.AnyKindTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#anyKindTest.
    def exitAnyKindTest(self, ctx:XQueryParser.AnyKindTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#binaryNodeTest.
    def enterBinaryNodeTest(self, ctx:XQueryParser.BinaryNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#binaryNodeTest.
    def exitBinaryNodeTest(self, ctx:XQueryParser.BinaryNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#documentTest.
    def enterDocumentTest(self, ctx:XQueryParser.DocumentTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#documentTest.
    def exitDocumentTest(self, ctx:XQueryParser.DocumentTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#textTest.
    def enterTextTest(self, ctx:XQueryParser.TextTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#textTest.
    def exitTextTest(self, ctx:XQueryParser.TextTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#commentTest.
    def enterCommentTest(self, ctx:XQueryParser.CommentTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#commentTest.
    def exitCommentTest(self, ctx:XQueryParser.CommentTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#namespaceNodeTest.
    def enterNamespaceNodeTest(self, ctx:XQueryParser.NamespaceNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#namespaceNodeTest.
    def exitNamespaceNodeTest(self, ctx:XQueryParser.NamespaceNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#piTest.
    def enterPiTest(self, ctx:XQueryParser.PiTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#piTest.
    def exitPiTest(self, ctx:XQueryParser.PiTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#attributeTest.
    def enterAttributeTest(self, ctx:XQueryParser.AttributeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#attributeTest.
    def exitAttributeTest(self, ctx:XQueryParser.AttributeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#attributeNameOrWildcard.
    def enterAttributeNameOrWildcard(self, ctx:XQueryParser.AttributeNameOrWildcardContext):
        pass

    # Exit a parse tree produced by XQueryParser#attributeNameOrWildcard.
    def exitAttributeNameOrWildcard(self, ctx:XQueryParser.AttributeNameOrWildcardContext):
        pass


    # Enter a parse tree produced by XQueryParser#schemaAttributeTest.
    def enterSchemaAttributeTest(self, ctx:XQueryParser.SchemaAttributeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#schemaAttributeTest.
    def exitSchemaAttributeTest(self, ctx:XQueryParser.SchemaAttributeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#elementTest.
    def enterElementTest(self, ctx:XQueryParser.ElementTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#elementTest.
    def exitElementTest(self, ctx:XQueryParser.ElementTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#elementNameOrWildcard.
    def enterElementNameOrWildcard(self, ctx:XQueryParser.ElementNameOrWildcardContext):
        pass

    # Exit a parse tree produced by XQueryParser#elementNameOrWildcard.
    def exitElementNameOrWildcard(self, ctx:XQueryParser.ElementNameOrWildcardContext):
        pass


    # Enter a parse tree produced by XQueryParser#schemaElementTest.
    def enterSchemaElementTest(self, ctx:XQueryParser.SchemaElementTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#schemaElementTest.
    def exitSchemaElementTest(self, ctx:XQueryParser.SchemaElementTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#elementDeclaration.
    def enterElementDeclaration(self, ctx:XQueryParser.ElementDeclarationContext):
        pass

    # Exit a parse tree produced by XQueryParser#elementDeclaration.
    def exitElementDeclaration(self, ctx:XQueryParser.ElementDeclarationContext):
        pass


    # Enter a parse tree produced by XQueryParser#attributeName.
    def enterAttributeName(self, ctx:XQueryParser.AttributeNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#attributeName.
    def exitAttributeName(self, ctx:XQueryParser.AttributeNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#elementName.
    def enterElementName(self, ctx:XQueryParser.ElementNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#elementName.
    def exitElementName(self, ctx:XQueryParser.ElementNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#simpleTypeName.
    def enterSimpleTypeName(self, ctx:XQueryParser.SimpleTypeNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#simpleTypeName.
    def exitSimpleTypeName(self, ctx:XQueryParser.SimpleTypeNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#typeName.
    def enterTypeName(self, ctx:XQueryParser.TypeNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#typeName.
    def exitTypeName(self, ctx:XQueryParser.TypeNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionTest.
    def enterFunctionTest(self, ctx:XQueryParser.FunctionTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionTest.
    def exitFunctionTest(self, ctx:XQueryParser.FunctionTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#anyFunctionTest.
    def enterAnyFunctionTest(self, ctx:XQueryParser.AnyFunctionTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#anyFunctionTest.
    def exitAnyFunctionTest(self, ctx:XQueryParser.AnyFunctionTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#typedFunctionTest.
    def enterTypedFunctionTest(self, ctx:XQueryParser.TypedFunctionTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#typedFunctionTest.
    def exitTypedFunctionTest(self, ctx:XQueryParser.TypedFunctionTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#mapTest.
    def enterMapTest(self, ctx:XQueryParser.MapTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mapTest.
    def exitMapTest(self, ctx:XQueryParser.MapTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#anyMapTest.
    def enterAnyMapTest(self, ctx:XQueryParser.AnyMapTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#anyMapTest.
    def exitAnyMapTest(self, ctx:XQueryParser.AnyMapTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#typedMapTest.
    def enterTypedMapTest(self, ctx:XQueryParser.TypedMapTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#typedMapTest.
    def exitTypedMapTest(self, ctx:XQueryParser.TypedMapTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#arrayTest.
    def enterArrayTest(self, ctx:XQueryParser.ArrayTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#arrayTest.
    def exitArrayTest(self, ctx:XQueryParser.ArrayTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#anyArrayTest.
    def enterAnyArrayTest(self, ctx:XQueryParser.AnyArrayTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#anyArrayTest.
    def exitAnyArrayTest(self, ctx:XQueryParser.AnyArrayTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#typedArrayTest.
    def enterTypedArrayTest(self, ctx:XQueryParser.TypedArrayTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#typedArrayTest.
    def exitTypedArrayTest(self, ctx:XQueryParser.TypedArrayTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#parenthesizedItemTest.
    def enterParenthesizedItemTest(self, ctx:XQueryParser.ParenthesizedItemTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#parenthesizedItemTest.
    def exitParenthesizedItemTest(self, ctx:XQueryParser.ParenthesizedItemTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#attributeDeclaration.
    def enterAttributeDeclaration(self, ctx:XQueryParser.AttributeDeclarationContext):
        pass

    # Exit a parse tree produced by XQueryParser#attributeDeclaration.
    def exitAttributeDeclaration(self, ctx:XQueryParser.AttributeDeclarationContext):
        pass


    # Enter a parse tree produced by XQueryParser#mlNodeTest.
    def enterMlNodeTest(self, ctx:XQueryParser.MlNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mlNodeTest.
    def exitMlNodeTest(self, ctx:XQueryParser.MlNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#mlArrayNodeTest.
    def enterMlArrayNodeTest(self, ctx:XQueryParser.MlArrayNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mlArrayNodeTest.
    def exitMlArrayNodeTest(self, ctx:XQueryParser.MlArrayNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#mlObjectNodeTest.
    def enterMlObjectNodeTest(self, ctx:XQueryParser.MlObjectNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mlObjectNodeTest.
    def exitMlObjectNodeTest(self, ctx:XQueryParser.MlObjectNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#mlNumberNodeTest.
    def enterMlNumberNodeTest(self, ctx:XQueryParser.MlNumberNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mlNumberNodeTest.
    def exitMlNumberNodeTest(self, ctx:XQueryParser.MlNumberNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#mlBooleanNodeTest.
    def enterMlBooleanNodeTest(self, ctx:XQueryParser.MlBooleanNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mlBooleanNodeTest.
    def exitMlBooleanNodeTest(self, ctx:XQueryParser.MlBooleanNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#mlNullNodeTest.
    def enterMlNullNodeTest(self, ctx:XQueryParser.MlNullNodeTestContext):
        pass

    # Exit a parse tree produced by XQueryParser#mlNullNodeTest.
    def exitMlNullNodeTest(self, ctx:XQueryParser.MlNullNodeTestContext):
        pass


    # Enter a parse tree produced by XQueryParser#eqName.
    def enterEqName(self, ctx:XQueryParser.EqNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#eqName.
    def exitEqName(self, ctx:XQueryParser.EqNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#qName.
    def enterQName(self, ctx:XQueryParser.QNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#qName.
    def exitQName(self, ctx:XQueryParser.QNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#ncName.
    def enterNcName(self, ctx:XQueryParser.NcNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#ncName.
    def exitNcName(self, ctx:XQueryParser.NcNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#functionName.
    def enterFunctionName(self, ctx:XQueryParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by XQueryParser#functionName.
    def exitFunctionName(self, ctx:XQueryParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by XQueryParser#keyword.
    def enterKeyword(self, ctx:XQueryParser.KeywordContext):
        pass

    # Exit a parse tree produced by XQueryParser#keyword.
    def exitKeyword(self, ctx:XQueryParser.KeywordContext):
        pass


    # Enter a parse tree produced by XQueryParser#keywordNotOKForFunction.
    def enterKeywordNotOKForFunction(self, ctx:XQueryParser.KeywordNotOKForFunctionContext):
        pass

    # Exit a parse tree produced by XQueryParser#keywordNotOKForFunction.
    def exitKeywordNotOKForFunction(self, ctx:XQueryParser.KeywordNotOKForFunctionContext):
        pass


    # Enter a parse tree produced by XQueryParser#keywordOKForFunction.
    def enterKeywordOKForFunction(self, ctx:XQueryParser.KeywordOKForFunctionContext):
        pass

    # Exit a parse tree produced by XQueryParser#keywordOKForFunction.
    def exitKeywordOKForFunction(self, ctx:XQueryParser.KeywordOKForFunctionContext):
        pass


    # Enter a parse tree produced by XQueryParser#uriLiteral.
    def enterUriLiteral(self, ctx:XQueryParser.UriLiteralContext):
        pass

    # Exit a parse tree produced by XQueryParser#uriLiteral.
    def exitUriLiteral(self, ctx:XQueryParser.UriLiteralContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringLiteralQuot.
    def enterStringLiteralQuot(self, ctx:XQueryParser.StringLiteralQuotContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringLiteralQuot.
    def exitStringLiteralQuot(self, ctx:XQueryParser.StringLiteralQuotContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringLiteralApos.
    def enterStringLiteralApos(self, ctx:XQueryParser.StringLiteralAposContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringLiteralApos.
    def exitStringLiteralApos(self, ctx:XQueryParser.StringLiteralAposContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringLiteral.
    def enterStringLiteral(self, ctx:XQueryParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringLiteral.
    def exitStringLiteral(self, ctx:XQueryParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringContentQuot.
    def enterStringContentQuot(self, ctx:XQueryParser.StringContentQuotContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringContentQuot.
    def exitStringContentQuot(self, ctx:XQueryParser.StringContentQuotContext):
        pass


    # Enter a parse tree produced by XQueryParser#stringContentApos.
    def enterStringContentApos(self, ctx:XQueryParser.StringContentAposContext):
        pass

    # Exit a parse tree produced by XQueryParser#stringContentApos.
    def exitStringContentApos(self, ctx:XQueryParser.StringContentAposContext):
        pass


    # Enter a parse tree produced by XQueryParser#noQuotesNoBracesNoAmpNoLAng.
    def enterNoQuotesNoBracesNoAmpNoLAng(self, ctx:XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext):
        pass

    # Exit a parse tree produced by XQueryParser#noQuotesNoBracesNoAmpNoLAng.
    def exitNoQuotesNoBracesNoAmpNoLAng(self, ctx:XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext):
        pass



del XQueryParser