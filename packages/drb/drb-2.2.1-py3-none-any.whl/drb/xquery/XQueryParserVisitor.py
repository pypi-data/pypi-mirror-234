# Generated from XQueryParser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .XQueryParser import XQueryParser
else:
    from XQueryParser import XQueryParser

# This class defines a complete generic visitor for a parse tree produced by XQueryParser.

class XQueryParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by XQueryParser#module.
    def visitModule(self, ctx:XQueryParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#xqDocComment.
    def visitXqDocComment(self, ctx:XQueryParser.XqDocCommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#versionDecl.
    def visitVersionDecl(self, ctx:XQueryParser.VersionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mainModule.
    def visitMainModule(self, ctx:XQueryParser.MainModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#queryBody.
    def visitQueryBody(self, ctx:XQueryParser.QueryBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#libraryModule.
    def visitLibraryModule(self, ctx:XQueryParser.LibraryModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#moduleDecl.
    def visitModuleDecl(self, ctx:XQueryParser.ModuleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#prolog.
    def visitProlog(self, ctx:XQueryParser.PrologContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#defaultNamespaceDecl.
    def visitDefaultNamespaceDecl(self, ctx:XQueryParser.DefaultNamespaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#setter.
    def visitSetter(self, ctx:XQueryParser.SetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#boundarySpaceDecl.
    def visitBoundarySpaceDecl(self, ctx:XQueryParser.BoundarySpaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#defaultCollationDecl.
    def visitDefaultCollationDecl(self, ctx:XQueryParser.DefaultCollationDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#baseURIDecl.
    def visitBaseURIDecl(self, ctx:XQueryParser.BaseURIDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#constructionDecl.
    def visitConstructionDecl(self, ctx:XQueryParser.ConstructionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#orderingModeDecl.
    def visitOrderingModeDecl(self, ctx:XQueryParser.OrderingModeDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#emptyOrderDecl.
    def visitEmptyOrderDecl(self, ctx:XQueryParser.EmptyOrderDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#copyNamespacesDecl.
    def visitCopyNamespacesDecl(self, ctx:XQueryParser.CopyNamespacesDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#preserveMode.
    def visitPreserveMode(self, ctx:XQueryParser.PreserveModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#inheritMode.
    def visitInheritMode(self, ctx:XQueryParser.InheritModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#decimalFormatDecl.
    def visitDecimalFormatDecl(self, ctx:XQueryParser.DecimalFormatDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#schemaImport.
    def visitSchemaImport(self, ctx:XQueryParser.SchemaImportContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#schemaPrefix.
    def visitSchemaPrefix(self, ctx:XQueryParser.SchemaPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#moduleImport.
    def visitModuleImport(self, ctx:XQueryParser.ModuleImportContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#namespaceDecl.
    def visitNamespaceDecl(self, ctx:XQueryParser.NamespaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#varDecl.
    def visitVarDecl(self, ctx:XQueryParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#varValue.
    def visitVarValue(self, ctx:XQueryParser.VarValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#varDefaultValue.
    def visitVarDefaultValue(self, ctx:XQueryParser.VarDefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#contextItemDecl.
    def visitContextItemDecl(self, ctx:XQueryParser.ContextItemDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionDecl.
    def visitFunctionDecl(self, ctx:XQueryParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionParams.
    def visitFunctionParams(self, ctx:XQueryParser.FunctionParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionParam.
    def visitFunctionParam(self, ctx:XQueryParser.FunctionParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#annotations.
    def visitAnnotations(self, ctx:XQueryParser.AnnotationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#annotation.
    def visitAnnotation(self, ctx:XQueryParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#annotList.
    def visitAnnotList(self, ctx:XQueryParser.AnnotListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#annotationParam.
    def visitAnnotationParam(self, ctx:XQueryParser.AnnotationParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionReturn.
    def visitFunctionReturn(self, ctx:XQueryParser.FunctionReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#optionDecl.
    def visitOptionDecl(self, ctx:XQueryParser.OptionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#expr.
    def visitExpr(self, ctx:XQueryParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#exprSingle.
    def visitExprSingle(self, ctx:XQueryParser.ExprSingleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#flworExpr.
    def visitFlworExpr(self, ctx:XQueryParser.FlworExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#initialClause.
    def visitInitialClause(self, ctx:XQueryParser.InitialClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#intermediateClause.
    def visitIntermediateClause(self, ctx:XQueryParser.IntermediateClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#forClause.
    def visitForClause(self, ctx:XQueryParser.ForClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#forBinding.
    def visitForBinding(self, ctx:XQueryParser.ForBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#allowingEmpty.
    def visitAllowingEmpty(self, ctx:XQueryParser.AllowingEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#positionalVar.
    def visitPositionalVar(self, ctx:XQueryParser.PositionalVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#letClause.
    def visitLetClause(self, ctx:XQueryParser.LetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#letBinding.
    def visitLetBinding(self, ctx:XQueryParser.LetBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#windowClause.
    def visitWindowClause(self, ctx:XQueryParser.WindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#tumblingWindowClause.
    def visitTumblingWindowClause(self, ctx:XQueryParser.TumblingWindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#slidingWindowClause.
    def visitSlidingWindowClause(self, ctx:XQueryParser.SlidingWindowClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#windowStartCondition.
    def visitWindowStartCondition(self, ctx:XQueryParser.WindowStartConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#windowEndCondition.
    def visitWindowEndCondition(self, ctx:XQueryParser.WindowEndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#windowVars.
    def visitWindowVars(self, ctx:XQueryParser.WindowVarsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#countClause.
    def visitCountClause(self, ctx:XQueryParser.CountClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#whereClause.
    def visitWhereClause(self, ctx:XQueryParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#groupByClause.
    def visitGroupByClause(self, ctx:XQueryParser.GroupByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#groupingSpecList.
    def visitGroupingSpecList(self, ctx:XQueryParser.GroupingSpecListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#groupingSpec.
    def visitGroupingSpec(self, ctx:XQueryParser.GroupingSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#orderByClause.
    def visitOrderByClause(self, ctx:XQueryParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#orderSpec.
    def visitOrderSpec(self, ctx:XQueryParser.OrderSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#returnClause.
    def visitReturnClause(self, ctx:XQueryParser.ReturnClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#quantifiedExpr.
    def visitQuantifiedExpr(self, ctx:XQueryParser.QuantifiedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#quantifiedVar.
    def visitQuantifiedVar(self, ctx:XQueryParser.QuantifiedVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#switchExpr.
    def visitSwitchExpr(self, ctx:XQueryParser.SwitchExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#switchCaseClause.
    def visitSwitchCaseClause(self, ctx:XQueryParser.SwitchCaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#switchCaseOperand.
    def visitSwitchCaseOperand(self, ctx:XQueryParser.SwitchCaseOperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#typeswitchExpr.
    def visitTypeswitchExpr(self, ctx:XQueryParser.TypeswitchExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#caseClause.
    def visitCaseClause(self, ctx:XQueryParser.CaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#sequenceUnionType.
    def visitSequenceUnionType(self, ctx:XQueryParser.SequenceUnionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#ifExpr.
    def visitIfExpr(self, ctx:XQueryParser.IfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#tryCatchExpr.
    def visitTryCatchExpr(self, ctx:XQueryParser.TryCatchExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#tryClause.
    def visitTryClause(self, ctx:XQueryParser.TryClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#enclosedTryTargetExpression.
    def visitEnclosedTryTargetExpression(self, ctx:XQueryParser.EnclosedTryTargetExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#catchClause.
    def visitCatchClause(self, ctx:XQueryParser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#enclosedExpression.
    def visitEnclosedExpression(self, ctx:XQueryParser.EnclosedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#catchErrorList.
    def visitCatchErrorList(self, ctx:XQueryParser.CatchErrorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#existUpdateExpr.
    def visitExistUpdateExpr(self, ctx:XQueryParser.ExistUpdateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#existReplaceExpr.
    def visitExistReplaceExpr(self, ctx:XQueryParser.ExistReplaceExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#existValueExpr.
    def visitExistValueExpr(self, ctx:XQueryParser.ExistValueExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#existInsertExpr.
    def visitExistInsertExpr(self, ctx:XQueryParser.ExistInsertExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#existDeleteExpr.
    def visitExistDeleteExpr(self, ctx:XQueryParser.ExistDeleteExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#existRenameExpr.
    def visitExistRenameExpr(self, ctx:XQueryParser.ExistRenameExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#orExpr.
    def visitOrExpr(self, ctx:XQueryParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#andExpr.
    def visitAndExpr(self, ctx:XQueryParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#comparisonExpr.
    def visitComparisonExpr(self, ctx:XQueryParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringConcatExpr.
    def visitStringConcatExpr(self, ctx:XQueryParser.StringConcatExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#rangeExpr.
    def visitRangeExpr(self, ctx:XQueryParser.RangeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:XQueryParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:XQueryParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#unionExpr.
    def visitUnionExpr(self, ctx:XQueryParser.UnionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#intersectExceptExpr.
    def visitIntersectExceptExpr(self, ctx:XQueryParser.IntersectExceptExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#instanceOfExpr.
    def visitInstanceOfExpr(self, ctx:XQueryParser.InstanceOfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#treatExpr.
    def visitTreatExpr(self, ctx:XQueryParser.TreatExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#castableExpr.
    def visitCastableExpr(self, ctx:XQueryParser.CastableExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#castExpr.
    def visitCastExpr(self, ctx:XQueryParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#arrowExpr.
    def visitArrowExpr(self, ctx:XQueryParser.ArrowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#unaryExpression.
    def visitUnaryExpression(self, ctx:XQueryParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#valueExpr.
    def visitValueExpr(self, ctx:XQueryParser.ValueExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#generalComp.
    def visitGeneralComp(self, ctx:XQueryParser.GeneralCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#valueComp.
    def visitValueComp(self, ctx:XQueryParser.ValueCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#nodeComp.
    def visitNodeComp(self, ctx:XQueryParser.NodeCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#validateExpr.
    def visitValidateExpr(self, ctx:XQueryParser.ValidateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#validationMode.
    def visitValidationMode(self, ctx:XQueryParser.ValidationModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#extensionExpr.
    def visitExtensionExpr(self, ctx:XQueryParser.ExtensionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#simpleMapExpr.
    def visitSimpleMapExpr(self, ctx:XQueryParser.SimpleMapExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#pathExpr.
    def visitPathExpr(self, ctx:XQueryParser.PathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#relativePathExpr.
    def visitRelativePathExpr(self, ctx:XQueryParser.RelativePathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stepExpr.
    def visitStepExpr(self, ctx:XQueryParser.StepExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#axisStep.
    def visitAxisStep(self, ctx:XQueryParser.AxisStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#forwardStep.
    def visitForwardStep(self, ctx:XQueryParser.ForwardStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#forwardAxis.
    def visitForwardAxis(self, ctx:XQueryParser.ForwardAxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#abbrevForwardStep.
    def visitAbbrevForwardStep(self, ctx:XQueryParser.AbbrevForwardStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#reverseStep.
    def visitReverseStep(self, ctx:XQueryParser.ReverseStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#reverseAxis.
    def visitReverseAxis(self, ctx:XQueryParser.ReverseAxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#abbrevReverseStep.
    def visitAbbrevReverseStep(self, ctx:XQueryParser.AbbrevReverseStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#nodeTest.
    def visitNodeTest(self, ctx:XQueryParser.NodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#nameTest.
    def visitNameTest(self, ctx:XQueryParser.NameTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#allNames.
    def visitAllNames(self, ctx:XQueryParser.AllNamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#allWithNS.
    def visitAllWithNS(self, ctx:XQueryParser.AllWithNSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#allWithLocal.
    def visitAllWithLocal(self, ctx:XQueryParser.AllWithLocalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#postfixExpr.
    def visitPostfixExpr(self, ctx:XQueryParser.PostfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#argumentList.
    def visitArgumentList(self, ctx:XQueryParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#predicateList.
    def visitPredicateList(self, ctx:XQueryParser.PredicateListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#predicate.
    def visitPredicate(self, ctx:XQueryParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#lookup.
    def visitLookup(self, ctx:XQueryParser.LookupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#keySpecifier.
    def visitKeySpecifier(self, ctx:XQueryParser.KeySpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#arrowFunctionSpecifier.
    def visitArrowFunctionSpecifier(self, ctx:XQueryParser.ArrowFunctionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:XQueryParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#literal.
    def visitLiteral(self, ctx:XQueryParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#numericLiteral.
    def visitNumericLiteral(self, ctx:XQueryParser.NumericLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#varRef.
    def visitVarRef(self, ctx:XQueryParser.VarRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#varName.
    def visitVarName(self, ctx:XQueryParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#parenthesizedExpr.
    def visitParenthesizedExpr(self, ctx:XQueryParser.ParenthesizedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#contextItemExpr.
    def visitContextItemExpr(self, ctx:XQueryParser.ContextItemExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#orderedExpr.
    def visitOrderedExpr(self, ctx:XQueryParser.OrderedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#unorderedExpr.
    def visitUnorderedExpr(self, ctx:XQueryParser.UnorderedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionCall.
    def visitFunctionCall(self, ctx:XQueryParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#argument.
    def visitArgument(self, ctx:XQueryParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#nodeConstructor.
    def visitNodeConstructor(self, ctx:XQueryParser.NodeConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#directConstructor.
    def visitDirectConstructor(self, ctx:XQueryParser.DirectConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirElemConstructorOpenClose.
    def visitDirElemConstructorOpenClose(self, ctx:XQueryParser.DirElemConstructorOpenCloseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirElemConstructorSingleTag.
    def visitDirElemConstructorSingleTag(self, ctx:XQueryParser.DirElemConstructorSingleTagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirAttributeList.
    def visitDirAttributeList(self, ctx:XQueryParser.DirAttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirAttributeValueApos.
    def visitDirAttributeValueApos(self, ctx:XQueryParser.DirAttributeValueAposContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirAttributeValueQuot.
    def visitDirAttributeValueQuot(self, ctx:XQueryParser.DirAttributeValueQuotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirAttributeValue.
    def visitDirAttributeValue(self, ctx:XQueryParser.DirAttributeValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirAttributeContentQuot.
    def visitDirAttributeContentQuot(self, ctx:XQueryParser.DirAttributeContentQuotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirAttributeContentApos.
    def visitDirAttributeContentApos(self, ctx:XQueryParser.DirAttributeContentAposContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#dirElemContent.
    def visitDirElemContent(self, ctx:XQueryParser.DirElemContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#commonContent.
    def visitCommonContent(self, ctx:XQueryParser.CommonContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#computedConstructor.
    def visitComputedConstructor(self, ctx:XQueryParser.ComputedConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compMLJSONConstructor.
    def visitCompMLJSONConstructor(self, ctx:XQueryParser.CompMLJSONConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compMLJSONArrayConstructor.
    def visitCompMLJSONArrayConstructor(self, ctx:XQueryParser.CompMLJSONArrayConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compMLJSONObjectConstructor.
    def visitCompMLJSONObjectConstructor(self, ctx:XQueryParser.CompMLJSONObjectConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compMLJSONNumberConstructor.
    def visitCompMLJSONNumberConstructor(self, ctx:XQueryParser.CompMLJSONNumberConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compMLJSONBooleanConstructor.
    def visitCompMLJSONBooleanConstructor(self, ctx:XQueryParser.CompMLJSONBooleanConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compMLJSONNullConstructor.
    def visitCompMLJSONNullConstructor(self, ctx:XQueryParser.CompMLJSONNullConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compBinaryConstructor.
    def visitCompBinaryConstructor(self, ctx:XQueryParser.CompBinaryConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compDocConstructor.
    def visitCompDocConstructor(self, ctx:XQueryParser.CompDocConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compElemConstructor.
    def visitCompElemConstructor(self, ctx:XQueryParser.CompElemConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#enclosedContentExpr.
    def visitEnclosedContentExpr(self, ctx:XQueryParser.EnclosedContentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compAttrConstructor.
    def visitCompAttrConstructor(self, ctx:XQueryParser.CompAttrConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compNamespaceConstructor.
    def visitCompNamespaceConstructor(self, ctx:XQueryParser.CompNamespaceConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#prefix.
    def visitPrefix(self, ctx:XQueryParser.PrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#enclosedPrefixExpr.
    def visitEnclosedPrefixExpr(self, ctx:XQueryParser.EnclosedPrefixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#enclosedURIExpr.
    def visitEnclosedURIExpr(self, ctx:XQueryParser.EnclosedURIExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compTextConstructor.
    def visitCompTextConstructor(self, ctx:XQueryParser.CompTextConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compCommentConstructor.
    def visitCompCommentConstructor(self, ctx:XQueryParser.CompCommentConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#compPIConstructor.
    def visitCompPIConstructor(self, ctx:XQueryParser.CompPIConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionItemExpr.
    def visitFunctionItemExpr(self, ctx:XQueryParser.FunctionItemExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#namedFunctionRef.
    def visitNamedFunctionRef(self, ctx:XQueryParser.NamedFunctionRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#inlineFunctionRef.
    def visitInlineFunctionRef(self, ctx:XQueryParser.InlineFunctionRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionBody.
    def visitFunctionBody(self, ctx:XQueryParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mapConstructor.
    def visitMapConstructor(self, ctx:XQueryParser.MapConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mapConstructorEntry.
    def visitMapConstructorEntry(self, ctx:XQueryParser.MapConstructorEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#arrayConstructor.
    def visitArrayConstructor(self, ctx:XQueryParser.ArrayConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#squareArrayConstructor.
    def visitSquareArrayConstructor(self, ctx:XQueryParser.SquareArrayConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#curlyArrayConstructor.
    def visitCurlyArrayConstructor(self, ctx:XQueryParser.CurlyArrayConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringConstructor.
    def visitStringConstructor(self, ctx:XQueryParser.StringConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringConstructorContent.
    def visitStringConstructorContent(self, ctx:XQueryParser.StringConstructorContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#charNoGrave.
    def visitCharNoGrave(self, ctx:XQueryParser.CharNoGraveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#charNoLBrace.
    def visitCharNoLBrace(self, ctx:XQueryParser.CharNoLBraceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#charNoRBrack.
    def visitCharNoRBrack(self, ctx:XQueryParser.CharNoRBrackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringConstructorChars.
    def visitStringConstructorChars(self, ctx:XQueryParser.StringConstructorCharsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringConstructorInterpolation.
    def visitStringConstructorInterpolation(self, ctx:XQueryParser.StringConstructorInterpolationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#unaryLookup.
    def visitUnaryLookup(self, ctx:XQueryParser.UnaryLookupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#singleType.
    def visitSingleType(self, ctx:XQueryParser.SingleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:XQueryParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#sequenceType.
    def visitSequenceType(self, ctx:XQueryParser.SequenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#itemType.
    def visitItemType(self, ctx:XQueryParser.ItemTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#atomicOrUnionType.
    def visitAtomicOrUnionType(self, ctx:XQueryParser.AtomicOrUnionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#kindTest.
    def visitKindTest(self, ctx:XQueryParser.KindTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#anyKindTest.
    def visitAnyKindTest(self, ctx:XQueryParser.AnyKindTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#binaryNodeTest.
    def visitBinaryNodeTest(self, ctx:XQueryParser.BinaryNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#documentTest.
    def visitDocumentTest(self, ctx:XQueryParser.DocumentTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#textTest.
    def visitTextTest(self, ctx:XQueryParser.TextTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#commentTest.
    def visitCommentTest(self, ctx:XQueryParser.CommentTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#namespaceNodeTest.
    def visitNamespaceNodeTest(self, ctx:XQueryParser.NamespaceNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#piTest.
    def visitPiTest(self, ctx:XQueryParser.PiTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#attributeTest.
    def visitAttributeTest(self, ctx:XQueryParser.AttributeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#attributeNameOrWildcard.
    def visitAttributeNameOrWildcard(self, ctx:XQueryParser.AttributeNameOrWildcardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#schemaAttributeTest.
    def visitSchemaAttributeTest(self, ctx:XQueryParser.SchemaAttributeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#elementTest.
    def visitElementTest(self, ctx:XQueryParser.ElementTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#elementNameOrWildcard.
    def visitElementNameOrWildcard(self, ctx:XQueryParser.ElementNameOrWildcardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#schemaElementTest.
    def visitSchemaElementTest(self, ctx:XQueryParser.SchemaElementTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#elementDeclaration.
    def visitElementDeclaration(self, ctx:XQueryParser.ElementDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#attributeName.
    def visitAttributeName(self, ctx:XQueryParser.AttributeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#elementName.
    def visitElementName(self, ctx:XQueryParser.ElementNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#simpleTypeName.
    def visitSimpleTypeName(self, ctx:XQueryParser.SimpleTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#typeName.
    def visitTypeName(self, ctx:XQueryParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionTest.
    def visitFunctionTest(self, ctx:XQueryParser.FunctionTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#anyFunctionTest.
    def visitAnyFunctionTest(self, ctx:XQueryParser.AnyFunctionTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#typedFunctionTest.
    def visitTypedFunctionTest(self, ctx:XQueryParser.TypedFunctionTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mapTest.
    def visitMapTest(self, ctx:XQueryParser.MapTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#anyMapTest.
    def visitAnyMapTest(self, ctx:XQueryParser.AnyMapTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#typedMapTest.
    def visitTypedMapTest(self, ctx:XQueryParser.TypedMapTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#arrayTest.
    def visitArrayTest(self, ctx:XQueryParser.ArrayTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#anyArrayTest.
    def visitAnyArrayTest(self, ctx:XQueryParser.AnyArrayTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#typedArrayTest.
    def visitTypedArrayTest(self, ctx:XQueryParser.TypedArrayTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#parenthesizedItemTest.
    def visitParenthesizedItemTest(self, ctx:XQueryParser.ParenthesizedItemTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#attributeDeclaration.
    def visitAttributeDeclaration(self, ctx:XQueryParser.AttributeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mlNodeTest.
    def visitMlNodeTest(self, ctx:XQueryParser.MlNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mlArrayNodeTest.
    def visitMlArrayNodeTest(self, ctx:XQueryParser.MlArrayNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mlObjectNodeTest.
    def visitMlObjectNodeTest(self, ctx:XQueryParser.MlObjectNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mlNumberNodeTest.
    def visitMlNumberNodeTest(self, ctx:XQueryParser.MlNumberNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mlBooleanNodeTest.
    def visitMlBooleanNodeTest(self, ctx:XQueryParser.MlBooleanNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#mlNullNodeTest.
    def visitMlNullNodeTest(self, ctx:XQueryParser.MlNullNodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#eqName.
    def visitEqName(self, ctx:XQueryParser.EqNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#qName.
    def visitQName(self, ctx:XQueryParser.QNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#ncName.
    def visitNcName(self, ctx:XQueryParser.NcNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#functionName.
    def visitFunctionName(self, ctx:XQueryParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#keyword.
    def visitKeyword(self, ctx:XQueryParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#keywordNotOKForFunction.
    def visitKeywordNotOKForFunction(self, ctx:XQueryParser.KeywordNotOKForFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#keywordOKForFunction.
    def visitKeywordOKForFunction(self, ctx:XQueryParser.KeywordOKForFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#uriLiteral.
    def visitUriLiteral(self, ctx:XQueryParser.UriLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringLiteralQuot.
    def visitStringLiteralQuot(self, ctx:XQueryParser.StringLiteralQuotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringLiteralApos.
    def visitStringLiteralApos(self, ctx:XQueryParser.StringLiteralAposContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringLiteral.
    def visitStringLiteral(self, ctx:XQueryParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringContentQuot.
    def visitStringContentQuot(self, ctx:XQueryParser.StringContentQuotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#stringContentApos.
    def visitStringContentApos(self, ctx:XQueryParser.StringContentAposContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XQueryParser#noQuotesNoBracesNoAmpNoLAng.
    def visitNoQuotesNoBracesNoAmpNoLAng(self, ctx:XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext):
        return self.visitChildren(ctx)



del XQueryParser