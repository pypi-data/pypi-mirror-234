# Generated from XQueryParser.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u00cd")
        buf.write("\u086a\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t")
        buf.write("&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.\t.\4")
        buf.write("/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t\64")
        buf.write("\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t")
        buf.write(";\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\t")
        buf.write("D\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\tL\4M\t")
        buf.write("M\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\tU\4V\t")
        buf.write("V\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4^\t^\4")
        buf.write("_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4g\tg\4")
        buf.write("h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4p\tp\4")
        buf.write("q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4y\ty\4")
        buf.write("z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\4\u0080\t\u0080")
        buf.write("\4\u0081\t\u0081\4\u0082\t\u0082\4\u0083\t\u0083\4\u0084")
        buf.write("\t\u0084\4\u0085\t\u0085\4\u0086\t\u0086\4\u0087\t\u0087")
        buf.write("\4\u0088\t\u0088\4\u0089\t\u0089\4\u008a\t\u008a\4\u008b")
        buf.write("\t\u008b\4\u008c\t\u008c\4\u008d\t\u008d\4\u008e\t\u008e")
        buf.write("\4\u008f\t\u008f\4\u0090\t\u0090\4\u0091\t\u0091\4\u0092")
        buf.write("\t\u0092\4\u0093\t\u0093\4\u0094\t\u0094\4\u0095\t\u0095")
        buf.write("\4\u0096\t\u0096\4\u0097\t\u0097\4\u0098\t\u0098\4\u0099")
        buf.write("\t\u0099\4\u009a\t\u009a\4\u009b\t\u009b\4\u009c\t\u009c")
        buf.write("\4\u009d\t\u009d\4\u009e\t\u009e\4\u009f\t\u009f\4\u00a0")
        buf.write("\t\u00a0\4\u00a1\t\u00a1\4\u00a2\t\u00a2\4\u00a3\t\u00a3")
        buf.write("\4\u00a4\t\u00a4\4\u00a5\t\u00a5\4\u00a6\t\u00a6\4\u00a7")
        buf.write("\t\u00a7\4\u00a8\t\u00a8\4\u00a9\t\u00a9\4\u00aa\t\u00aa")
        buf.write("\4\u00ab\t\u00ab\4\u00ac\t\u00ac\4\u00ad\t\u00ad\4\u00ae")
        buf.write("\t\u00ae\4\u00af\t\u00af\4\u00b0\t\u00b0\4\u00b1\t\u00b1")
        buf.write("\4\u00b2\t\u00b2\4\u00b3\t\u00b3\4\u00b4\t\u00b4\4\u00b5")
        buf.write("\t\u00b5\4\u00b6\t\u00b6\4\u00b7\t\u00b7\4\u00b8\t\u00b8")
        buf.write("\4\u00b9\t\u00b9\4\u00ba\t\u00ba\4\u00bb\t\u00bb\4\u00bc")
        buf.write("\t\u00bc\4\u00bd\t\u00bd\4\u00be\t\u00be\4\u00bf\t\u00bf")
        buf.write("\4\u00c0\t\u00c0\4\u00c1\t\u00c1\4\u00c2\t\u00c2\4\u00c3")
        buf.write("\t\u00c3\4\u00c4\t\u00c4\4\u00c5\t\u00c5\4\u00c6\t\u00c6")
        buf.write("\4\u00c7\t\u00c7\4\u00c8\t\u00c8\4\u00c9\t\u00c9\4\u00ca")
        buf.write("\t\u00ca\4\u00cb\t\u00cb\4\u00cc\t\u00cc\4\u00cd\t\u00cd")
        buf.write("\4\u00ce\t\u00ce\4\u00cf\t\u00cf\4\u00d0\t\u00d0\4\u00d1")
        buf.write("\t\u00d1\4\u00d2\t\u00d2\4\u00d3\t\u00d3\4\u00d4\t\u00d4")
        buf.write("\4\u00d5\t\u00d5\4\u00d6\t\u00d6\4\u00d7\t\u00d7\4\u00d8")
        buf.write("\t\u00d8\4\u00d9\t\u00d9\4\u00da\t\u00da\4\u00db\t\u00db")
        buf.write("\4\u00dc\t\u00dc\4\u00dd\t\u00dd\4\u00de\t\u00de\4\u00df")
        buf.write("\t\u00df\4\u00e0\t\u00e0\4\u00e1\t\u00e1\4\u00e2\t\u00e2")
        buf.write("\4\u00e3\t\u00e3\4\u00e4\t\u00e4\4\u00e5\t\u00e5\4\u00e6")
        buf.write("\t\u00e6\4\u00e7\t\u00e7\4\u00e8\t\u00e8\4\u00e9\t\u00e9")
        buf.write("\4\u00ea\t\u00ea\4\u00eb\t\u00eb\4\u00ec\t\u00ec\4\u00ed")
        buf.write("\t\u00ed\4\u00ee\t\u00ee\4\u00ef\t\u00ef\4\u00f0\t\u00f0")
        buf.write("\4\u00f1\t\u00f1\3\2\5\2\u01e4\n\2\3\2\5\2\u01e7\n\2\3")
        buf.write("\2\5\2\u01ea\n\2\3\2\3\2\3\2\3\2\5\2\u01f0\n\2\3\2\7\2")
        buf.write("\u01f3\n\2\f\2\16\2\u01f6\13\2\5\2\u01f8\n\2\3\3\3\3\3")
        buf.write("\4\3\4\3\4\3\4\3\4\5\4\u0201\n\4\3\4\3\4\3\5\3\5\3\5\3")
        buf.write("\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3\t")
        buf.write("\3\t\3\t\3\t\5\t\u0219\n\t\3\t\3\t\7\t\u021d\n\t\f\t\16")
        buf.write("\t\u0220\13\t\3\t\5\t\u0223\n\t\3\t\3\t\3\t\3\t\5\t\u0229")
        buf.write("\n\t\3\t\3\t\7\t\u022d\n\t\f\t\16\t\u0230\13\t\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3")
        buf.write("\13\5\13\u0240\n\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3")
        buf.write("\r\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\20\3\20\3")
        buf.write("\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22")
        buf.write("\3\22\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\25")
        buf.write("\3\25\5\25\u026c\n\25\3\25\3\25\3\25\7\25\u0271\n\25\f")
        buf.write("\25\16\25\u0274\13\25\3\26\3\26\3\26\5\26\u0279\n\26\3")
        buf.write("\26\3\26\3\26\3\26\3\26\7\26\u0280\n\26\f\26\16\26\u0283")
        buf.write("\13\26\5\26\u0285\n\26\3\27\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\5\27\u028e\n\27\3\30\3\30\3\30\3\30\3\30\3\30\5\30")
        buf.write("\u0296\n\30\3\30\3\30\3\30\3\30\3\30\7\30\u029d\n\30\f")
        buf.write("\30\16\30\u02a0\13\30\5\30\u02a2\n\30\3\31\3\31\3\31\3")
        buf.write("\31\3\31\3\31\3\32\3\32\3\32\5\32\u02ad\n\32\3\32\3\32")
        buf.write("\3\32\3\32\5\32\u02b3\n\32\3\32\3\32\3\32\3\32\3\32\5")
        buf.write("\32\u02ba\n\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\5\32\u02c5\n\32\5\32\u02c7\n\32\3\33\3\33\3\34\3")
        buf.write("\34\3\35\3\35\3\35\3\35\3\35\5\35\u02d2\n\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\5\35\u02d9\n\35\5\35\u02db\n\35\3\36\3")
        buf.write("\36\3\36\5\36\u02e0\n\36\3\36\3\36\3\36\3\36\5\36\u02e6")
        buf.write("\n\36\3\36\3\36\5\36\u02ea\n\36\3\36\3\36\5\36\u02ee\n")
        buf.write("\36\3\37\3\37\3\37\7\37\u02f3\n\37\f\37\16\37\u02f6\13")
        buf.write("\37\3 \3 \3 \5 \u02fb\n \3!\7!\u02fe\n!\f!\16!\u0301\13")
        buf.write("!\3\"\3\"\3\"\3\"\3\"\3\"\5\"\u0309\n\"\3#\3#\3#\7#\u030e")
        buf.write("\n#\f#\16#\u0311\13#\3$\3$\3%\3%\3%\3&\3&\3&\3&\3&\3\'")
        buf.write("\3\'\3\'\7\'\u0320\n\'\f\'\16\'\u0323\13\'\3(\3(\3(\3")
        buf.write("(\3(\3(\3(\3(\5(\u032d\n(\3)\3)\7)\u0331\n)\f)\16)\u0334")
        buf.write("\13)\3)\3)\3*\3*\3*\5*\u033b\n*\3+\3+\3+\3+\3+\5+\u0342")
        buf.write("\n+\3,\3,\3,\3,\7,\u0348\n,\f,\16,\u034b\13,\3-\3-\3-")
        buf.write("\5-\u0350\n-\3-\5-\u0353\n-\3-\5-\u0356\n-\3-\3-\3-\3")
        buf.write(".\3.\3.\3/\3/\3/\3/\3\60\3\60\3\60\3\60\7\60\u0366\n\60")
        buf.write("\f\60\16\60\u0369\13\60\3\61\3\61\3\61\5\61\u036e\n\61")
        buf.write("\3\61\3\61\3\61\3\62\3\62\3\62\5\62\u0376\n\62\3\63\3")
        buf.write("\63\3\63\3\63\3\63\5\63\u037d\n\63\3\63\3\63\3\63\3\63")
        buf.write("\5\63\u0383\n\63\3\64\3\64\3\64\3\64\3\64\5\64\u038a\n")
        buf.write("\64\3\64\3\64\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65")
        buf.write("\3\66\5\66\u0397\n\66\3\66\3\66\3\66\3\66\3\66\3\67\3")
        buf.write("\67\5\67\u03a0\n\67\3\67\5\67\u03a3\n\67\3\67\3\67\3\67")
        buf.write("\5\67\u03a8\n\67\3\67\3\67\3\67\5\67\u03ad\n\67\38\38")
        buf.write("\38\38\39\39\39\3:\3:\3:\3:\3;\3;\3;\7;\u03bd\n;\f;\16")
        buf.write(";\u03c0\13;\3<\3<\3<\5<\u03c5\n<\3<\3<\5<\u03c9\n<\3<")
        buf.write("\3<\5<\u03cd\n<\3=\5=\u03d0\n=\3=\3=\3=\3=\3=\7=\u03d7")
        buf.write("\n=\f=\16=\u03da\13=\3>\3>\5>\u03de\n>\3>\3>\5>\u03e2")
        buf.write("\n>\3>\3>\5>\u03e6\n>\3?\3?\3?\3@\3@\3@\3@\7@\u03ef\n")
        buf.write("@\f@\16@\u03f2\13@\3@\3@\3@\3A\3A\3A\5A\u03fa\nA\3A\3")
        buf.write("A\3A\3B\3B\3B\3B\3B\6B\u0404\nB\rB\16B\u0405\3B\3B\3B")
        buf.write("\3B\3C\3C\6C\u040e\nC\rC\16C\u040f\3C\3C\3C\3D\3D\3E\3")
        buf.write("E\3E\3E\3E\6E\u041c\nE\rE\16E\u041d\3E\3E\3E\5E\u0423")
        buf.write("\nE\3E\3E\3E\3F\3F\3F\3F\3F\5F\u042d\nF\3F\3F\3F\3F\3")
        buf.write("G\3G\3G\7G\u0436\nG\fG\16G\u0439\13G\3H\3H\3H\3H\3H\3")
        buf.write("H\3H\3H\3H\3I\3I\6I\u0446\nI\rI\16I\u0447\3J\3J\3J\3K")
        buf.write("\3K\3L\3L\3L\3L\3L\3L\3L\5L\u0456\nL\3L\3L\3M\3M\5M\u045c")
        buf.write("\nM\3M\3M\3N\3N\3N\7N\u0463\nN\fN\16N\u0466\13N\3O\3O")
        buf.write("\3O\3O\3O\3O\5O\u046e\nO\3P\3P\3P\3P\3P\3Q\3Q\3Q\3Q\3")
        buf.write("Q\3R\3R\3R\3R\3R\3S\3S\3S\3T\3T\3T\3T\3T\3U\3U\3U\7U\u048a")
        buf.write("\nU\fU\16U\u048d\13U\3V\3V\3V\7V\u0492\nV\fV\16V\u0495")
        buf.write("\13V\3W\3W\3W\3W\5W\u049b\nW\3W\3W\5W\u049f\nW\3X\3X\3")
        buf.write("X\7X\u04a4\nX\fX\16X\u04a7\13X\3Y\3Y\3Y\5Y\u04ac\nY\3")
        buf.write("Z\3Z\3Z\7Z\u04b1\nZ\fZ\16Z\u04b4\13Z\3[\3[\3[\7[\u04b9")
        buf.write("\n[\f[\16[\u04bc\13[\3\\\3\\\3\\\7\\\u04c1\n\\\f\\\16")
        buf.write("\\\u04c4\13\\\3]\3]\3]\7]\u04c9\n]\f]\16]\u04cc\13]\3")
        buf.write("^\3^\3^\3^\5^\u04d2\n^\3_\3_\3_\3_\5_\u04d8\n_\3`\3`\3")
        buf.write("`\3`\5`\u04de\n`\3a\3a\3a\3a\5a\u04e4\na\3b\3b\3b\3b\3")
        buf.write("b\7b\u04eb\nb\fb\16b\u04ee\13b\3c\7c\u04f1\nc\fc\16c\u04f4")
        buf.write("\13c\3c\3c\3d\3d\3d\5d\u04fb\nd\3e\3e\3e\3e\3e\3e\3e\3")
        buf.write("e\5e\u0505\ne\3f\3f\3g\3g\3g\3g\3g\5g\u050e\ng\3h\3h\3")
        buf.write("h\3h\5h\u0514\nh\3h\3h\3i\3i\3j\6j\u051b\nj\rj\16j\u051c")
        buf.write("\3j\3j\3j\3j\3k\3k\3k\7k\u0526\nk\fk\16k\u0529\13k\3l")
        buf.write("\3l\5l\u052d\nl\3l\3l\3l\5l\u0532\nl\3m\3m\3m\7m\u0537")
        buf.write("\nm\fm\16m\u053a\13m\3n\3n\5n\u053e\nn\3o\3o\5o\u0542")
        buf.write("\no\3o\3o\3p\3p\3p\3p\5p\u054a\np\3q\3q\3q\3q\3r\5r\u0551")
        buf.write("\nr\3r\3r\3s\3s\3s\3s\5s\u0559\ns\3t\3t\3t\3t\3u\3u\3")
        buf.write("v\3v\5v\u0563\nv\3w\3w\5w\u0567\nw\3x\3x\3x\5x\u056c\n")
        buf.write("x\3y\3y\3y\3y\7y\u0572\ny\fy\16y\u0575\13y\3z\3z\3z\3")
        buf.write("z\7z\u057b\nz\fz\16z\u057e\13z\5z\u0580\nz\3z\3z\3{\7")
        buf.write("{\u0585\n{\f{\16{\u0588\13{\3|\3|\3|\3|\3}\3}\3}\3~\3")
        buf.write("~\3~\3~\5~\u0595\n~\3\177\3\177\3\177\5\177\u059a\n\177")
        buf.write("\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080")
        buf.write("\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080\5\u0080")
        buf.write("\u05a9\n\u0080\3\u0081\3\u0081\5\u0081\u05ad\n\u0081\3")
        buf.write("\u0082\3\u0082\3\u0083\3\u0083\3\u0083\3\u0084\3\u0084")
        buf.write("\3\u0085\3\u0085\5\u0085\u05b8\n\u0085\3\u0085\3\u0085")
        buf.write("\3\u0086\3\u0086\3\u0087\3\u0087\3\u0087\3\u0088\3\u0088")
        buf.write("\3\u0088\3\u0089\3\u0089\3\u0089\3\u008a\3\u008a\5\u008a")
        buf.write("\u05c9\n\u008a\3\u008b\3\u008b\5\u008b\u05cd\n\u008b\3")
        buf.write("\u008c\3\u008c\3\u008c\5\u008c\u05d2\n\u008c\3\u008d\3")
        buf.write("\u008d\3\u008d\3\u008d\3\u008d\7\u008d\u05d9\n\u008d\f")
        buf.write("\u008d\16\u008d\u05dc\13\u008d\3\u008d\3\u008d\3\u008d")
        buf.write("\3\u008d\3\u008d\3\u008e\3\u008e\3\u008e\3\u008e\3\u008e")
        buf.write("\3\u008e\3\u008f\3\u008f\3\u008f\3\u008f\7\u008f\u05ed")
        buf.write("\n\u008f\f\u008f\16\u008f\u05f0\13\u008f\3\u0090\3\u0090")
        buf.write("\3\u0090\3\u0090\3\u0090\7\u0090\u05f7\n\u0090\f\u0090")
        buf.write("\16\u0090\u05fa\13\u0090\3\u0090\3\u0090\3\u0091\3\u0091")
        buf.write("\3\u0091\3\u0091\3\u0091\7\u0091\u0603\n\u0091\f\u0091")
        buf.write("\16\u0091\u0606\13\u0091\3\u0091\3\u0091\3\u0092\3\u0092")
        buf.write("\5\u0092\u060c\n\u0092\3\u0093\6\u0093\u060f\n\u0093\r")
        buf.write("\u0093\16\u0093\u0610\3\u0093\3\u0093\3\u0093\3\u0093")
        buf.write("\3\u0093\5\u0093\u0618\n\u0093\3\u0093\5\u0093\u061b\n")
        buf.write("\u0093\3\u0094\6\u0094\u061e\n\u0094\r\u0094\16\u0094")
        buf.write("\u061f\3\u0094\3\u0094\3\u0094\3\u0094\3\u0094\5\u0094")
        buf.write("\u0627\n\u0094\3\u0094\5\u0094\u062a\n\u0094\3\u0095\3")
        buf.write("\u0095\3\u0095\3\u0095\3\u0095\3\u0095\5\u0095\u0632\n")
        buf.write("\u0095\3\u0096\3\u0096\3\u0096\3\u0096\3\u0096\3\u0096")
        buf.write("\3\u0096\3\u0096\3\u0096\5\u0096\u063d\n\u0096\3\u0097")
        buf.write("\3\u0097\3\u0097\3\u0097\3\u0097\3\u0097\3\u0097\3\u0097")
        buf.write("\5\u0097\u0647\n\u0097\3\u0098\3\u0098\3\u0098\3\u0098")
        buf.write("\3\u0098\3\u0098\5\u0098\u064f\n\u0098\3\u0099\3\u0099")
        buf.write("\3\u0099\3\u009a\3\u009a\3\u009a\3\u009a\3\u009a\3\u009a")
        buf.write("\3\u009a\3\u009a\3\u009a\3\u009a\7\u009a\u065e\n\u009a")
        buf.write("\f\u009a\16\u009a\u0661\13\u009a\5\u009a\u0663\n\u009a")
        buf.write("\3\u009a\3\u009a\3\u009b\3\u009b\3\u009b\3\u009c\3\u009c")
        buf.write("\3\u009c\3\u009c\3\u009c\3\u009d\3\u009d\3\u009d\3\u009d")
        buf.write("\3\u009e\3\u009e\3\u009e\3\u009f\3\u009f\3\u009f\3\u00a0")
        buf.write("\3\u00a0\3\u00a0\3\u00a0\3\u00a0\3\u00a0\5\u00a0\u067f")
        buf.write("\n\u00a0\3\u00a0\3\u00a0\3\u00a1\3\u00a1\3\u00a2\3\u00a2")
        buf.write("\3\u00a2\3\u00a2\3\u00a2\3\u00a2\5\u00a2\u068b\n\u00a2")
        buf.write("\3\u00a2\3\u00a2\3\u00a3\3\u00a3\3\u00a3\5\u00a3\u0692")
        buf.write("\n\u00a3\3\u00a3\3\u00a3\3\u00a4\3\u00a4\3\u00a5\3\u00a5")
        buf.write("\3\u00a6\3\u00a6\3\u00a7\3\u00a7\3\u00a7\3\u00a8\3\u00a8")
        buf.write("\3\u00a8\3\u00a9\3\u00a9\3\u00a9\3\u00a9\3\u00a9\3\u00a9")
        buf.write("\5\u00a9\u06a8\n\u00a9\3\u00a9\3\u00a9\3\u00aa\3\u00aa")
        buf.write("\5\u00aa\u06ae\n\u00aa\3\u00ab\3\u00ab\3\u00ab\3\u00ab")
        buf.write("\3\u00ac\3\u00ac\3\u00ac\3\u00ac\5\u00ac\u06b8\n\u00ac")
        buf.write("\3\u00ac\3\u00ac\3\u00ac\5\u00ac\u06bd\n\u00ac\3\u00ac")
        buf.write("\3\u00ac\3\u00ad\3\u00ad\3\u00ae\3\u00ae\3\u00ae\3\u00ae")
        buf.write("\3\u00ae\7\u00ae\u06c8\n\u00ae\f\u00ae\16\u00ae\u06cb")
        buf.write("\13\u00ae\5\u00ae\u06cd\n\u00ae\3\u00ae\3\u00ae\3\u00af")
        buf.write("\3\u00af\3\u00af\3\u00af\3\u00b0\3\u00b0\5\u00b0\u06d7")
        buf.write("\n\u00b0\3\u00b1\3\u00b1\3\u00b1\3\u00b1\7\u00b1\u06dd")
        buf.write("\n\u00b1\f\u00b1\16\u00b1\u06e0\13\u00b1\5\u00b1\u06e2")
        buf.write("\n\u00b1\3\u00b1\3\u00b1\3\u00b2\3\u00b2\3\u00b2\3\u00b3")
        buf.write("\3\u00b3\3\u00b3\3\u00b3\3\u00b4\3\u00b4\3\u00b4\3\u00b4")
        buf.write("\7\u00b4\u06f1\n\u00b4\f\u00b4\16\u00b4\u06f4\13\u00b4")
        buf.write("\3\u00b5\3\u00b5\3\u00b6\3\u00b6\3\u00b7\3\u00b7\3\u00b8")
        buf.write("\3\u00b8\3\u00b8\3\u00b8\3\u00b8\3\u00b8\3\u00b8\3\u00b8")
        buf.write("\3\u00b8\3\u00b8\7\u00b8\u0706\n\u00b8\f\u00b8\16\u00b8")
        buf.write("\u0709\13\u00b8\3\u00b9\3\u00b9\3\u00b9\3\u00b9\3\u00ba")
        buf.write("\3\u00ba\3\u00ba\3\u00bb\3\u00bb\5\u00bb\u0714\n\u00bb")
        buf.write("\3\u00bc\3\u00bc\3\u00bc\3\u00bd\3\u00bd\3\u00bd\3\u00bd")
        buf.write("\3\u00bd\5\u00bd\u071e\n\u00bd\5\u00bd\u0720\n\u00bd\3")
        buf.write("\u00be\3\u00be\3\u00be\3\u00be\3\u00be\3\u00be\3\u00be")
        buf.write("\3\u00be\3\u00be\5\u00be\u072b\n\u00be\3\u00bf\3\u00bf")
        buf.write("\3\u00c0\3\u00c0\3\u00c0\3\u00c0\3\u00c0\3\u00c0\3\u00c0")
        buf.write("\3\u00c0\3\u00c0\3\u00c0\3\u00c0\3\u00c0\5\u00c0\u073b")
        buf.write("\n\u00c0\3\u00c1\3\u00c1\3\u00c1\5\u00c1\u0740\n\u00c1")
        buf.write("\3\u00c1\3\u00c1\3\u00c2\3\u00c2\3\u00c2\3\u00c2\3\u00c3")
        buf.write("\3\u00c3\3\u00c3\3\u00c3\5\u00c3\u074c\n\u00c3\3\u00c3")
        buf.write("\3\u00c3\3\u00c4\3\u00c4\3\u00c4\3\u00c4\3\u00c5\3\u00c5")
        buf.write("\3\u00c5\3\u00c5\3\u00c6\3\u00c6\3\u00c6\3\u00c6\3\u00c7")
        buf.write("\3\u00c7\3\u00c7\3\u00c7\5\u00c7\u0760\n\u00c7\3\u00c7")
        buf.write("\3\u00c7\3\u00c8\3\u00c8\3\u00c8\3\u00c8\3\u00c8\5\u00c8")
        buf.write("\u0769\n\u00c8\5\u00c8\u076b\n\u00c8\3\u00c8\3\u00c8\3")
        buf.write("\u00c9\3\u00c9\5\u00c9\u0771\n\u00c9\3\u00ca\3\u00ca\3")
        buf.write("\u00ca\3\u00ca\3\u00ca\3\u00cb\3\u00cb\3\u00cb\3\u00cb")
        buf.write("\3\u00cb\3\u00cb\5\u00cb\u077e\n\u00cb\5\u00cb\u0780\n")
        buf.write("\u00cb\5\u00cb\u0782\n\u00cb\3\u00cb\3\u00cb\3\u00cc\3")
        buf.write("\u00cc\5\u00cc\u0788\n\u00cc\3\u00cd\3\u00cd\3\u00cd\3")
        buf.write("\u00cd\3\u00cd\3\u00ce\3\u00ce\3\u00cf\3\u00cf\3\u00d0")
        buf.write("\3\u00d0\3\u00d1\3\u00d1\3\u00d2\3\u00d2\3\u00d3\7\u00d3")
        buf.write("\u079a\n\u00d3\f\u00d3\16\u00d3\u079d\13\u00d3\3\u00d3")
        buf.write("\3\u00d3\5\u00d3\u07a1\n\u00d3\3\u00d4\3\u00d4\3\u00d4")
        buf.write("\3\u00d4\3\u00d4\3\u00d5\3\u00d5\3\u00d5\3\u00d5\3\u00d5")
        buf.write("\7\u00d5\u07ad\n\u00d5\f\u00d5\16\u00d5\u07b0\13\u00d5")
        buf.write("\5\u00d5\u07b2\n\u00d5\3\u00d5\3\u00d5\3\u00d5\3\u00d5")
        buf.write("\3\u00d6\3\u00d6\5\u00d6\u07ba\n\u00d6\3\u00d7\3\u00d7")
        buf.write("\3\u00d7\3\u00d7\3\u00d7\3\u00d8\3\u00d8\3\u00d8\3\u00d8")
        buf.write("\3\u00d8\3\u00d8\3\u00d8\3\u00d9\3\u00d9\5\u00d9\u07ca")
        buf.write("\n\u00d9\3\u00da\3\u00da\3\u00da\3\u00da\3\u00da\3\u00db")
        buf.write("\3\u00db\3\u00db\3\u00db\3\u00db\3\u00dc\3\u00dc\3\u00dc")
        buf.write("\3\u00dc\3\u00dd\3\u00dd\3\u00de\3\u00de\3\u00de\3\u00de")
        buf.write("\3\u00de\5\u00de\u07e1\n\u00de\3\u00df\3\u00df\3\u00df")
        buf.write("\5\u00df\u07e6\n\u00df\3\u00df\3\u00df\3\u00e0\3\u00e0")
        buf.write("\3\u00e0\5\u00e0\u07ed\n\u00e0\3\u00e0\3\u00e0\3\u00e1")
        buf.write("\3\u00e1\3\u00e1\5\u00e1\u07f4\n\u00e1\3\u00e1\3\u00e1")
        buf.write("\3\u00e2\3\u00e2\3\u00e2\5\u00e2\u07fb\n\u00e2\3\u00e2")
        buf.write("\3\u00e2\3\u00e3\3\u00e3\3\u00e3\5\u00e3\u0802\n\u00e3")
        buf.write("\3\u00e3\3\u00e3\3\u00e4\3\u00e4\5\u00e4\u0808\n\u00e4")
        buf.write("\3\u00e5\3\u00e5\5\u00e5\u080c\n\u00e5\3\u00e6\3\u00e6")
        buf.write("\5\u00e6\u0810\n\u00e6\3\u00e7\3\u00e7\3\u00e7\3\u00e7")
        buf.write("\5\u00e7\u0816\n\u00e7\3\u00e8\3\u00e8\5\u00e8\u081a\n")
        buf.write("\u00e8\3\u00e9\3\u00e9\3\u00ea\3\u00ea\3\u00eb\3\u00eb")
        buf.write("\3\u00ec\3\u00ec\3\u00ec\3\u00ec\3\u00ec\7\u00ec\u0827")
        buf.write("\n\u00ec\f\u00ec\16\u00ec\u082a\13\u00ec\3\u00ec\3\u00ec")
        buf.write("\3\u00ed\3\u00ed\3\u00ed\3\u00ed\3\u00ed\7\u00ed\u0833")
        buf.write("\n\u00ed\f\u00ed\16\u00ed\u0836\13\u00ed\3\u00ed\3\u00ed")
        buf.write("\3\u00ee\3\u00ee\5\u00ee\u083c\n\u00ee\3\u00ef\6\u00ef")
        buf.write("\u083f\n\u00ef\r\u00ef\16\u00ef\u0840\3\u00ef\3\u00ef")
        buf.write("\5\u00ef\u0845\n\u00ef\3\u00ef\5\u00ef\u0848\n\u00ef\3")
        buf.write("\u00ef\3\u00ef\3\u00ef\3\u00ef\3\u00ef\5\u00ef\u084f\n")
        buf.write("\u00ef\3\u00f0\6\u00f0\u0852\n\u00f0\r\u00f0\16\u00f0")
        buf.write("\u0853\3\u00f0\3\u00f0\5\u00f0\u0858\n\u00f0\3\u00f0\5")
        buf.write("\u00f0\u085b\n\u00f0\3\u00f0\3\u00f0\3\u00f0\3\u00f0\3")
        buf.write("\u00f0\5\u00f0\u0862\n\u00f0\3\u00f1\3\u00f1\6\u00f1\u0866")
        buf.write("\n\u00f1\r\u00f1\16\u00f1\u0867\3\u00f1\2\2\u00f2\2\4")
        buf.write("\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64")
        buf.write("\668:<>@BDFHJLNPRTVXZ\\^`bdfhjlnprtvxz|~\u0080\u0082\u0084")
        buf.write("\u0086\u0088\u008a\u008c\u008e\u0090\u0092\u0094\u0096")
        buf.write("\u0098\u009a\u009c\u009e\u00a0\u00a2\u00a4\u00a6\u00a8")
        buf.write("\u00aa\u00ac\u00ae\u00b0\u00b2\u00b4\u00b6\u00b8\u00ba")
        buf.write("\u00bc\u00be\u00c0\u00c2\u00c4\u00c6\u00c8\u00ca\u00cc")
        buf.write("\u00ce\u00d0\u00d2\u00d4\u00d6\u00d8\u00da\u00dc\u00de")
        buf.write("\u00e0\u00e2\u00e4\u00e6\u00e8\u00ea\u00ec\u00ee\u00f0")
        buf.write("\u00f2\u00f4\u00f6\u00f8\u00fa\u00fc\u00fe\u0100\u0102")
        buf.write("\u0104\u0106\u0108\u010a\u010c\u010e\u0110\u0112\u0114")
        buf.write("\u0116\u0118\u011a\u011c\u011e\u0120\u0122\u0124\u0126")
        buf.write("\u0128\u012a\u012c\u012e\u0130\u0132\u0134\u0136\u0138")
        buf.write("\u013a\u013c\u013e\u0140\u0142\u0144\u0146\u0148\u014a")
        buf.write("\u014c\u014e\u0150\u0152\u0154\u0156\u0158\u015a\u015c")
        buf.write("\u015e\u0160\u0162\u0164\u0166\u0168\u016a\u016c\u016e")
        buf.write("\u0170\u0172\u0174\u0176\u0178\u017a\u017c\u017e\u0180")
        buf.write("\u0182\u0184\u0186\u0188\u018a\u018c\u018e\u0190\u0192")
        buf.write("\u0194\u0196\u0198\u019a\u019c\u019e\u01a0\u01a2\u01a4")
        buf.write("\u01a6\u01a8\u01aa\u01ac\u01ae\u01b0\u01b2\u01b4\u01b6")
        buf.write("\u01b8\u01ba\u01bc\u01be\u01c0\u01c2\u01c4\u01c6\u01c8")
        buf.write("\u01ca\u01cc\u01ce\u01d0\u01d2\u01d4\u01d6\u01d8\u01da")
        buf.write("\u01dc\u01de\u01e0\2 \4\2XXee\4\2\u008c\u008c\u009a\u009a")
        buf.write("\4\2\u0087\u0087\u00a5\u00a5\4\2gguu\4\2\u0080\u0080\u008c")
        buf.write("\u008c\4\2nn\177\177\4\2==SS\4\2__\u0096\u0096\5\2bb\u008a")
        buf.write("\u008a\u00b7\u00b7\3\2\36\37\6\2\35\35UUjjyy\4\2))\u00a4")
        buf.write("\u00a4\4\2``pp\b\2^^ffiittww||\4\2<<\u00a2\u00a2\4\2s")
        buf.write("s\u0099\u0099\3\2&\'\7\2??HHQRbc\u0094\u0094\4\289\u0089")
        buf.write("\u008b\3\2\7\t\4\2\17\17\21\21\3\2\13\f\3\2#$\4\2\32\33")
        buf.write("\u00c7\u00c7\5\2\32\32\64\64\u00c7\u00c7\5\2\33\33\64")
        buf.write("\64\u00c7\u00c7\4\2\35\36,,\36\2\n\n\67\67;;??BBGGJJL")
        buf.write("LNNTTWX[[]]kkrrxx}~\u0081\u0081\u0083\u0083\u008e\u008e")
        buf.write("\u0092\u0093\u0095\u0095\u009b\u009c\u00a0\u00a3\u00a6")
        buf.write("\u00a6\u00aa\u00aa\u00ac\u00ac\u00ae\u00b9\34\28:<>@A")
        buf.write("CFHIKKMMOSUVYZ\\\\^jlqswy|\177\u0080\u0082\u0082\u0084")
        buf.write("\u008c\u008f\u0091\u0094\u0094\u0096\u009a\u009d\u009f")
        buf.write("\u00a4\u00a5\u00a7\u00a9\u00ab\u00ab\u00ad\u00ad\r\2\7")
        buf.write("\t\17\17\23\23\25\32\35)+\64\66\66}}\u008d\u008d\u00ba")
        buf.write("\u00bf\u00c6\u00c6\2\u08be\2\u01e3\3\2\2\2\4\u01f9\3\2")
        buf.write("\2\2\6\u01fb\3\2\2\2\b\u0204\3\2\2\2\n\u0207\3\2\2\2\f")
        buf.write("\u0209\3\2\2\2\16\u020c\3\2\2\2\20\u021e\3\2\2\2\22\u0231")
        buf.write("\3\2\2\2\24\u023f\3\2\2\2\26\u0241\3\2\2\2\30\u0245\3")
        buf.write("\2\2\2\32\u024a\3\2\2\2\34\u024e\3\2\2\2\36\u0252\3\2")
        buf.write("\2\2 \u0256\3\2\2\2\"\u025c\3\2\2\2$\u0262\3\2\2\2&\u0264")
        buf.write("\3\2\2\2(\u0266\3\2\2\2*\u0275\3\2\2\2,\u028d\3\2\2\2")
        buf.write(".\u028f\3\2\2\2\60\u02a3\3\2\2\2\62\u02a9\3\2\2\2\64\u02c8")
        buf.write("\3\2\2\2\66\u02ca\3\2\2\28\u02cc\3\2\2\2:\u02dc\3\2\2")
        buf.write("\2<\u02ef\3\2\2\2>\u02f7\3\2\2\2@\u02ff\3\2\2\2B\u0302")
        buf.write("\3\2\2\2D\u030a\3\2\2\2F\u0312\3\2\2\2H\u0314\3\2\2\2")
        buf.write("J\u0317\3\2\2\2L\u031c\3\2\2\2N\u032c\3\2\2\2P\u032e\3")
        buf.write("\2\2\2R\u033a\3\2\2\2T\u0341\3\2\2\2V\u0343\3\2\2\2X\u034c")
        buf.write("\3\2\2\2Z\u035a\3\2\2\2\\\u035d\3\2\2\2^\u0361\3\2\2\2")
        buf.write("`\u036a\3\2\2\2b\u0372\3\2\2\2d\u0377\3\2\2\2f\u0384\3")
        buf.write("\2\2\2h\u0390\3\2\2\2j\u0396\3\2\2\2l\u039f\3\2\2\2n\u03ae")
        buf.write("\3\2\2\2p\u03b2\3\2\2\2r\u03b5\3\2\2\2t\u03b9\3\2\2\2")
        buf.write("v\u03c1\3\2\2\2x\u03cf\3\2\2\2z\u03db\3\2\2\2|\u03e7\3")
        buf.write("\2\2\2~\u03ea\3\2\2\2\u0080\u03f6\3\2\2\2\u0082\u03fe")
        buf.write("\3\2\2\2\u0084\u040d\3\2\2\2\u0086\u0414\3\2\2\2\u0088")
        buf.write("\u0416\3\2\2\2\u008a\u0427\3\2\2\2\u008c\u0432\3\2\2\2")
        buf.write("\u008e\u043a\3\2\2\2\u0090\u0443\3\2\2\2\u0092\u0449\3")
        buf.write("\2\2\2\u0094\u044c\3\2\2\2\u0096\u044e\3\2\2\2\u0098\u0459")
        buf.write("\3\2\2\2\u009a\u045f\3\2\2\2\u009c\u0467\3\2\2\2\u009e")
        buf.write("\u046f\3\2\2\2\u00a0\u0474\3\2\2\2\u00a2\u0479\3\2\2\2")
        buf.write("\u00a4\u047e\3\2\2\2\u00a6\u0481\3\2\2\2\u00a8\u0486\3")
        buf.write("\2\2\2\u00aa\u048e\3\2\2\2\u00ac\u0496\3\2\2\2\u00ae\u04a0")
        buf.write("\3\2\2\2\u00b0\u04a8\3\2\2\2\u00b2\u04ad\3\2\2\2\u00b4")
        buf.write("\u04b5\3\2\2\2\u00b6\u04bd\3\2\2\2\u00b8\u04c5\3\2\2\2")
        buf.write("\u00ba\u04cd\3\2\2\2\u00bc\u04d3\3\2\2\2\u00be\u04d9\3")
        buf.write("\2\2\2\u00c0\u04df\3\2\2\2\u00c2\u04e5\3\2\2\2\u00c4\u04f2")
        buf.write("\3\2\2\2\u00c6\u04fa\3\2\2\2\u00c8\u0504\3\2\2\2\u00ca")
        buf.write("\u0506\3\2\2\2\u00cc\u050d\3\2\2\2\u00ce\u050f\3\2\2\2")
        buf.write("\u00d0\u0517\3\2\2\2\u00d2\u051a\3\2\2\2\u00d4\u0522\3")
        buf.write("\2\2\2\u00d6\u0531\3\2\2\2\u00d8\u0533\3\2\2\2\u00da\u053d")
        buf.write("\3\2\2\2\u00dc\u0541\3\2\2\2\u00de\u0549\3\2\2\2\u00e0")
        buf.write("\u054b\3\2\2\2\u00e2\u0550\3\2\2\2\u00e4\u0558\3\2\2\2")
        buf.write("\u00e6\u055a\3\2\2\2\u00e8\u055e\3\2\2\2\u00ea\u0562\3")
        buf.write("\2\2\2\u00ec\u0566\3\2\2\2\u00ee\u056b\3\2\2\2\u00f0\u056d")
        buf.write("\3\2\2\2\u00f2\u0576\3\2\2\2\u00f4\u0586\3\2\2\2\u00f6")
        buf.write("\u0589\3\2\2\2\u00f8\u058d\3\2\2\2\u00fa\u0594\3\2\2\2")
        buf.write("\u00fc\u0599\3\2\2\2\u00fe\u05a8\3\2\2\2\u0100\u05ac\3")
        buf.write("\2\2\2\u0102\u05ae\3\2\2\2\u0104\u05b0\3\2\2\2\u0106\u05b3")
        buf.write("\3\2\2\2\u0108\u05b5\3\2\2\2\u010a\u05bb\3\2\2\2\u010c")
        buf.write("\u05bd\3\2\2\2\u010e\u05c0\3\2\2\2\u0110\u05c3\3\2\2\2")
        buf.write("\u0112\u05c8\3\2\2\2\u0114\u05cc\3\2\2\2\u0116\u05d1\3")
        buf.write("\2\2\2\u0118\u05d3\3\2\2\2\u011a\u05e2\3\2\2\2\u011c\u05ee")
        buf.write("\3\2\2\2\u011e\u05f1\3\2\2\2\u0120\u05fd\3\2\2\2\u0122")
        buf.write("\u060b\3\2\2\2\u0124\u061a\3\2\2\2\u0126\u0629\3\2\2\2")
        buf.write("\u0128\u0631\3\2\2\2\u012a\u063c\3\2\2\2\u012c\u0646\3")
        buf.write("\2\2\2\u012e\u064e\3\2\2\2\u0130\u0650\3\2\2\2\u0132\u0653")
        buf.write("\3\2\2\2\u0134\u0666\3\2\2\2\u0136\u0669\3\2\2\2\u0138")
        buf.write("\u066e\3\2\2\2\u013a\u0672\3\2\2\2\u013c\u0675\3\2\2\2")
        buf.write("\u013e\u0678\3\2\2\2\u0140\u0682\3\2\2\2\u0142\u0684\3")
        buf.write("\2\2\2\u0144\u068e\3\2\2\2\u0146\u0695\3\2\2\2\u0148\u0697")
        buf.write("\3\2\2\2\u014a\u0699\3\2\2\2\u014c\u069b\3\2\2\2\u014e")
        buf.write("\u069e\3\2\2\2\u0150\u06a1\3\2\2\2\u0152\u06ad\3\2\2\2")
        buf.write("\u0154\u06af\3\2\2\2\u0156\u06b3\3\2\2\2\u0158\u06c0\3")
        buf.write("\2\2\2\u015a\u06c2\3\2\2\2\u015c\u06d0\3\2\2\2\u015e\u06d6")
        buf.write("\3\2\2\2\u0160\u06d8\3\2\2\2\u0162\u06e5\3\2\2\2\u0164")
        buf.write("\u06e8\3\2\2\2\u0166\u06ec\3\2\2\2\u0168\u06f5\3\2\2\2")
        buf.write("\u016a\u06f7\3\2\2\2\u016c\u06f9\3\2\2\2\u016e\u0707\3")
        buf.write("\2\2\2\u0170\u070a\3\2\2\2\u0172\u070e\3\2\2\2\u0174\u0711")
        buf.write("\3\2\2\2\u0176\u0715\3\2\2\2\u0178\u071f\3\2\2\2\u017a")
        buf.write("\u072a\3\2\2\2\u017c\u072c\3\2\2\2\u017e\u073a\3\2\2\2")
        buf.write("\u0180\u073c\3\2\2\2\u0182\u0743\3\2\2\2\u0184\u0747\3")
        buf.write("\2\2\2\u0186\u074f\3\2\2\2\u0188\u0753\3\2\2\2\u018a\u0757")
        buf.write("\3\2\2\2\u018c\u075b\3\2\2\2\u018e\u0763\3\2\2\2\u0190")
        buf.write("\u0770\3\2\2\2\u0192\u0772\3\2\2\2\u0194\u0777\3\2\2\2")
        buf.write("\u0196\u0787\3\2\2\2\u0198\u0789\3\2\2\2\u019a\u078e\3")
        buf.write("\2\2\2\u019c\u0790\3\2\2\2\u019e\u0792\3\2\2\2\u01a0\u0794")
        buf.write("\3\2\2\2\u01a2\u0796\3\2\2\2\u01a4\u079b\3\2\2\2\u01a6")
        buf.write("\u07a2\3\2\2\2\u01a8\u07a7\3\2\2\2\u01aa\u07b9\3\2\2\2")
        buf.write("\u01ac\u07bb\3\2\2\2\u01ae\u07c0\3\2\2\2\u01b0\u07c9\3")
        buf.write("\2\2\2\u01b2\u07cb\3\2\2\2\u01b4\u07d0\3\2\2\2\u01b6\u07d5")
        buf.write("\3\2\2\2\u01b8\u07d9\3\2\2\2\u01ba\u07e0\3\2\2\2\u01bc")
        buf.write("\u07e2\3\2\2\2\u01be\u07e9\3\2\2\2\u01c0\u07f0\3\2\2\2")
        buf.write("\u01c2\u07f7\3\2\2\2\u01c4\u07fe\3\2\2\2\u01c6\u0807\3")
        buf.write("\2\2\2\u01c8\u080b\3\2\2\2\u01ca\u080f\3\2\2\2\u01cc\u0815")
        buf.write("\3\2\2\2\u01ce\u0819\3\2\2\2\u01d0\u081b\3\2\2\2\u01d2")
        buf.write("\u081d\3\2\2\2\u01d4\u081f\3\2\2\2\u01d6\u0821\3\2\2\2")
        buf.write("\u01d8\u082d\3\2\2\2\u01da\u083b\3\2\2\2\u01dc\u084e\3")
        buf.write("\2\2\2\u01de\u0861\3\2\2\2\u01e0\u0865\3\2\2\2\u01e2\u01e4")
        buf.write("\5\4\3\2\u01e3\u01e2\3\2\2\2\u01e3\u01e4\3\2\2\2\u01e4")
        buf.write("\u01e6\3\2\2\2\u01e5\u01e7\5\6\4\2\u01e6\u01e5\3\2\2\2")
        buf.write("\u01e6\u01e7\3\2\2\2\u01e7\u01e9\3\2\2\2\u01e8\u01ea\5")
        buf.write("\4\3\2\u01e9\u01e8\3\2\2\2\u01e9\u01ea\3\2\2\2\u01ea\u01f7")
        buf.write("\3\2\2\2\u01eb\u01f8\5\f\7\2\u01ec\u01f4\5\b\5\2\u01ed")
        buf.write("\u01ef\7%\2\2\u01ee\u01f0\5\6\4\2\u01ef\u01ee\3\2\2\2")
        buf.write("\u01ef\u01f0\3\2\2\2\u01f0\u01f1\3\2\2\2\u01f1\u01f3\5")
        buf.write("\b\5\2\u01f2\u01ed\3\2\2\2\u01f3\u01f6\3\2\2\2\u01f4\u01f2")
        buf.write("\3\2\2\2\u01f4\u01f5\3\2\2\2\u01f5\u01f8\3\2\2\2\u01f6")
        buf.write("\u01f4\3\2\2\2\u01f7\u01eb\3\2\2\2\u01f7\u01ec\3\2\2\2")
        buf.write("\u01f8\3\3\2\2\2\u01f9\u01fa\7\u00c1\2\2\u01fa\5\3\2\2")
        buf.write("\2\u01fb\u01fc\7\u00ad\2\2\u01fc\u01fd\7\u00a9\2\2\u01fd")
        buf.write("\u0200\5\u01da\u00ee\2\u01fe\u01ff\7\\\2\2\u01ff\u0201")
        buf.write("\5\u01da\u00ee\2\u0200\u01fe\3\2\2\2\u0200\u0201\3\2\2")
        buf.write("\2\u0201\u0202\3\2\2\2\u0202\u0203\7%\2\2\u0203\7\3\2")
        buf.write("\2\2\u0204\u0205\5\20\t\2\u0205\u0206\5\n\6\2\u0206\t")
        buf.write("\3\2\2\2\u0207\u0208\5L\'\2\u0208\13\3\2\2\2\u0209\u020a")
        buf.write("\5\16\b\2\u020a\u020b\5\20\t\2\u020b\r\3\2\2\2\u020c\u020d")
        buf.write("\7z\2\2\u020d\u020e\7{\2\2\u020e\u020f\5\u01ca\u00e6\2")
        buf.write("\u020f\u0210\7\25\2\2\u0210\u0211\5\u01da\u00ee\2\u0211")
        buf.write("\u0212\7%\2\2\u0212\17\3\2\2\2\u0213\u0219\5\22\n\2\u0214")
        buf.write("\u0219\5\24\13\2\u0215\u0219\5\60\31\2\u0216\u0219\5*")
        buf.write("\26\2\u0217\u0219\5.\30\2\u0218\u0213\3\2\2\2\u0218\u0214")
        buf.write("\3\2\2\2\u0218\u0215\3\2\2\2\u0218\u0216\3\2\2\2\u0218")
        buf.write("\u0217\3\2\2\2\u0219\u021a\3\2\2\2\u021a\u021b\7%\2\2")
        buf.write("\u021b\u021d\3\2\2\2\u021c\u0218\3\2\2\2\u021d\u0220\3")
        buf.write("\2\2\2\u021e\u021c\3\2\2\2\u021e\u021f\3\2\2\2\u021f\u022e")
        buf.write("\3\2\2\2\u0220\u021e\3\2\2\2\u0221\u0223\5\4\3\2\u0222")
        buf.write("\u0221\3\2\2\2\u0222\u0223\3\2\2\2\u0223\u0228\3\2\2\2")
        buf.write("\u0224\u0229\5\62\32\2\u0225\u0229\5:\36\2\u0226\u0229")
        buf.write("\58\35\2\u0227\u0229\5J&\2\u0228\u0224\3\2\2\2\u0228\u0225")
        buf.write("\3\2\2\2\u0228\u0226\3\2\2\2\u0228\u0227\3\2\2\2\u0229")
        buf.write("\u022a\3\2\2\2\u022a\u022b\7%\2\2\u022b\u022d\3\2\2\2")
        buf.write("\u022c\u0222\3\2\2\2\u022d\u0230\3\2\2\2\u022e\u022c\3")
        buf.write("\2\2\2\u022e\u022f\3\2\2\2\u022f\21\3\2\2\2\u0230\u022e")
        buf.write("\3\2\2\2\u0231\u0232\7O\2\2\u0232\u0233\7P\2\2\u0233\u0234")
        buf.write("\t\2\2\2\u0234\u0235\7{\2\2\u0235\u0236\5\u01da\u00ee")
        buf.write("\2\u0236\23\3\2\2\2\u0237\u0240\5\26\f\2\u0238\u0240\5")
        buf.write("\30\r\2\u0239\u0240\5\32\16\2\u023a\u0240\5\34\17\2\u023b")
        buf.write("\u0240\5\36\20\2\u023c\u0240\5 \21\2\u023d\u0240\5\"\22")
        buf.write("\2\u023e\u0240\5(\25\2\u023f\u0237\3\2\2\2\u023f\u0238")
        buf.write("\3\2\2\2\u023f\u0239\3\2\2\2\u023f\u023a\3\2\2\2\u023f")
        buf.write("\u023b\3\2\2\2\u023f\u023c\3\2\2\2\u023f\u023d\3\2\2\2")
        buf.write("\u023f\u023e\3\2\2\2\u0240\25\3\2\2\2\u0241\u0242\7O\2")
        buf.write("\2\u0242\u0243\7A\2\2\u0243\u0244\t\3\2\2\u0244\27\3\2")
        buf.write("\2\2\u0245\u0246\7O\2\2\u0246\u0247\7P\2\2\u0247\u0248")
        buf.write("\7I\2\2\u0248\u0249\5\u01d4\u00eb\2\u0249\31\3\2\2\2\u024a")
        buf.write("\u024b\7O\2\2\u024b\u024c\7@\2\2\u024c\u024d\5\u01d4\u00eb")
        buf.write("\2\u024d\33\3\2\2\2\u024e\u024f\7O\2\2\u024f\u0250\7K")
        buf.write("\2\2\u0250\u0251\t\3\2\2\u0251\35\3\2\2\2\u0252\u0253")
        buf.write("\7O\2\2\u0253\u0254\7\u0088\2\2\u0254\u0255\t\4\2\2\u0255")
        buf.write("\37\3\2\2\2\u0256\u0257\7O\2\2\u0257\u0258\7P\2\2\u0258")
        buf.write("\u0259\7\u0086\2\2\u0259\u025a\7Z\2\2\u025a\u025b\t\5")
        buf.write("\2\2\u025b!\3\2\2\2\u025c\u025d\7O\2\2\u025d\u025e\7M")
        buf.write("\2\2\u025e\u025f\5$\23\2\u025f\u0260\7 \2\2\u0260\u0261")
        buf.write("\5&\24\2\u0261#\3\2\2\2\u0262\u0263\t\6\2\2\u0263%\3\2")
        buf.write("\2\2\u0264\u0265\t\7\2\2\u0265\'\3\2\2\2\u0266\u026b\7")
        buf.write("O\2\2\u0267\u0268\7T\2\2\u0268\u026c\5\u01c6\u00e4\2\u0269")
        buf.write("\u026a\7P\2\2\u026a\u026c\7T\2\2\u026b\u0267\3\2\2\2\u026b")
        buf.write("\u0269\3\2\2\2\u026c\u0272\3\2\2\2\u026d\u026e\7\n\2\2")
        buf.write("\u026e\u026f\7\25\2\2\u026f\u0271\5\u01da\u00ee\2\u0270")
        buf.write("\u026d\3\2\2\2\u0271\u0274\3\2\2\2\u0272\u0270\3\2\2\2")
        buf.write("\u0272\u0273\3\2\2\2\u0273)\3\2\2\2\u0274\u0272\3\2\2")
        buf.write("\2\u0275\u0276\7l\2\2\u0276\u0278\7\u0091\2\2\u0277\u0279")
        buf.write("\5,\27\2\u0278\u0277\3\2\2\2\u0278\u0279\3\2\2\2\u0279")
        buf.write("\u027a\3\2\2\2\u027a\u0284\5\u01d4\u00eb\2\u027b\u027c")
        buf.write("\7>\2\2\u027c\u0281\5\u01d4\u00eb\2\u027d\u027e\7 \2\2")
        buf.write("\u027e\u0280\5\u01d4\u00eb\2\u027f\u027d\3\2\2\2\u0280")
        buf.write("\u0283\3\2\2\2\u0281\u027f\3\2\2\2\u0281\u0282\3\2\2\2")
        buf.write("\u0282\u0285\3\2\2\2\u0283\u0281\3\2\2\2\u0284\u027b\3")
        buf.write("\2\2\2\u0284\u0285\3\2\2\2\u0285+\3\2\2\2\u0286\u0287")
        buf.write("\7{\2\2\u0287\u0288\5\u01ca\u00e6\2\u0288\u0289\7\25\2")
        buf.write("\2\u0289\u028e\3\2\2\2\u028a\u028b\7P\2\2\u028b\u028c")
        buf.write("\7X\2\2\u028c\u028e\7{\2\2\u028d\u0286\3\2\2\2\u028d\u028a")
        buf.write("\3\2\2\2\u028e-\3\2\2\2\u028f\u0290\7l\2\2\u0290\u0295")
        buf.write("\7z\2\2\u0291\u0292\7{\2\2\u0292\u0293\5\u01ca\u00e6\2")
        buf.write("\u0293\u0294\7\25\2\2\u0294\u0296\3\2\2\2\u0295\u0291")
        buf.write("\3\2\2\2\u0295\u0296\3\2\2\2\u0296\u0297\3\2\2\2\u0297")
        buf.write("\u02a1\5\u01d4\u00eb\2\u0298\u0299\7>\2\2\u0299\u029e")
        buf.write("\5\u01d4\u00eb\2\u029a\u029b\7 \2\2\u029b\u029d\5\u01d4")
        buf.write("\u00eb\2\u029c\u029a\3\2\2\2\u029d\u02a0\3\2\2\2\u029e")
        buf.write("\u029c\3\2\2\2\u029e\u029f\3\2\2\2\u029f\u02a2\3\2\2\2")
        buf.write("\u02a0\u029e\3\2\2\2\u02a1\u0298\3\2\2\2\u02a1\u02a2\3")
        buf.write("\2\2\2\u02a2/\3\2\2\2\u02a3\u02a4\7O\2\2\u02a4\u02a5\7")
        buf.write("{\2\2\u02a5\u02a6\5\u01ca\u00e6\2\u02a6\u02a7\7\25\2\2")
        buf.write("\u02a7\u02a8\5\u01d4\u00eb\2\u02a8\61\3\2\2\2\u02a9\u02ac")
        buf.write("\7O\2\2\u02aa\u02ad\5@!\2\u02ab\u02ad\5\u01ca\u00e6\2")
        buf.write("\u02ac\u02aa\3\2\2\2\u02ac\u02ab\3\2\2\2\u02ad\u02ae\3")
        buf.write("\2\2\2\u02ae\u02af\7\u00a8\2\2\u02af\u02b0\7.\2\2\u02b0")
        buf.write("\u02b2\5\u0106\u0084\2\u02b1\u02b3\5\u0176\u00bc\2\u02b2")
        buf.write("\u02b1\3\2\2\2\u02b2\u02b3\3\2\2\2\u02b3\u02c6\3\2\2\2")
        buf.write("\u02b4\u02b5\7$\2\2\u02b5\u02c7\5\64\33\2\u02b6\u02b9")
        buf.write("\7a\2\2\u02b7\u02b8\7$\2\2\u02b8\u02ba\5\66\34\2\u02b9")
        buf.write("\u02b7\3\2\2\2\u02b9\u02ba\3\2\2\2\u02ba\u02c7\3\2\2\2")
        buf.write("\u02bb\u02bc\7\33\2\2\u02bc\u02bd\5\64\33\2\u02bd\u02be")
        buf.write("\7\34\2\2\u02be\u02c7\3\2\2\2\u02bf\u02c4\7a\2\2\u02c0")
        buf.write("\u02c1\7\33\2\2\u02c1\u02c2\5\66\34\2\u02c2\u02c3\7\34")
        buf.write("\2\2\u02c3\u02c5\3\2\2\2\u02c4\u02c0\3\2\2\2\u02c4\u02c5")
        buf.write("\3\2\2\2\u02c5\u02c7\3\2\2\2\u02c6\u02b4\3\2\2\2\u02c6")
        buf.write("\u02b6\3\2\2\2\u02c6\u02bb\3\2\2\2\u02c6\u02bf\3\2\2\2")
        buf.write("\u02c7\63\3\2\2\2\u02c8\u02c9\5L\'\2\u02c9\65\3\2\2\2")
        buf.write("\u02ca\u02cb\5L\'\2\u02cb\67\3\2\2\2\u02cc\u02cd\7O\2")
        buf.write("\2\u02cd\u02ce\7L\2\2\u02ce\u02d1\7r\2\2\u02cf\u02d0\7")
        buf.write("<\2\2\u02d0\u02d2\5\u017a\u00be\2\u02d1\u02cf\3\2\2\2")
        buf.write("\u02d1\u02d2\3\2\2\2\u02d2\u02da\3\2\2\2\u02d3\u02d4\7")
        buf.write("$\2\2\u02d4\u02db\5N(\2\u02d5\u02d8\7a\2\2\u02d6\u02d7")
        buf.write("\7$\2\2\u02d7\u02d9\5N(\2\u02d8\u02d6\3\2\2\2\u02d8\u02d9")
        buf.write("\3\2\2\2\u02d9\u02db\3\2\2\2\u02da\u02d3\3\2\2\2\u02da")
        buf.write("\u02d5\3\2\2\2\u02db9\3\2\2\2\u02dc\u02df\7O\2\2\u02dd")
        buf.write("\u02e0\5@!\2\u02de\u02e0\5\u01ca\u00e6\2\u02df\u02dd\3")
        buf.write("\2\2\2\u02df\u02de\3\2\2\2\u02e0\u02e1\3\2\2\2\u02e1\u02e2")
        buf.write("\7e\2\2\u02e2\u02e3\5\u01c6\u00e4\2\u02e3\u02e5\7\27\2")
        buf.write("\2\u02e4\u02e6\5<\37\2\u02e5\u02e4\3\2\2\2\u02e5\u02e6")
        buf.write("\3\2\2\2\u02e6\u02e7\3\2\2\2\u02e7\u02e9\7\30\2\2\u02e8")
        buf.write("\u02ea\5H%\2\u02e9\u02e8\3\2\2\2\u02e9\u02ea\3\2\2\2\u02ea")
        buf.write("\u02ed\3\2\2\2\u02eb\u02ee\5\u0158\u00ad\2\u02ec\u02ee")
        buf.write("\7a\2\2\u02ed\u02eb\3\2\2\2\u02ed\u02ec\3\2\2\2\u02ee")
        buf.write(";\3\2\2\2\u02ef\u02f4\5> \2\u02f0\u02f1\7 \2\2\u02f1\u02f3")
        buf.write("\5> \2\u02f2\u02f0\3\2\2\2\u02f3\u02f6\3\2\2\2\u02f4\u02f2")
        buf.write("\3\2\2\2\u02f4\u02f5\3\2\2\2\u02f5=\3\2\2\2\u02f6\u02f4")
        buf.write("\3\2\2\2\u02f7\u02f8\7.\2\2\u02f8\u02fa\5\u01c8\u00e5")
        buf.write("\2\u02f9\u02fb\5\u0176\u00bc\2\u02fa\u02f9\3\2\2\2\u02fa")
        buf.write("\u02fb\3\2\2\2\u02fb?\3\2\2\2\u02fc\u02fe\5B\"\2\u02fd")
        buf.write("\u02fc\3\2\2\2\u02fe\u0301\3\2\2\2\u02ff\u02fd\3\2\2\2")
        buf.write("\u02ff\u0300\3\2\2\2\u0300A\3\2\2\2\u0301\u02ff\3\2\2")
        buf.write("\2\u0302\u0303\7/\2\2\u0303\u0308\5\u01c8\u00e5\2\u0304")
        buf.write("\u0305\7\27\2\2\u0305\u0306\5D#\2\u0306\u0307\7\30\2\2")
        buf.write("\u0307\u0309\3\2\2\2\u0308\u0304\3\2\2\2\u0308\u0309\3")
        buf.write("\2\2\2\u0309C\3\2\2\2\u030a\u030f\5F$\2\u030b\u030c\7")
        buf.write(" \2\2\u030c\u030e\5F$\2\u030d\u030b\3\2\2\2\u030e\u0311")
        buf.write("\3\2\2\2\u030f\u030d\3\2\2\2\u030f\u0310\3\2\2\2\u0310")
        buf.write("E\3\2\2\2\u0311\u030f\3\2\2\2\u0312\u0313\5\u0100\u0081")
        buf.write("\2\u0313G\3\2\2\2\u0314\u0315\7<\2\2\u0315\u0316\5\u0178")
        buf.write("\u00bd\2\u0316I\3\2\2\2\u0317\u0318\7O\2\2\u0318\u0319")
        buf.write("\7\u0084\2\2\u0319\u031a\5\u01c8\u00e5\2\u031a\u031b\5")
        buf.write("\u01da\u00ee\2\u031bK\3\2\2\2\u031c\u0321\5N(\2\u031d")
        buf.write("\u031e\7 \2\2\u031e\u0320\5N(\2\u031f\u031d\3\2\2\2\u0320")
        buf.write("\u0323\3\2\2\2\u0321\u031f\3\2\2\2\u0321\u0322\3\2\2\2")
        buf.write("\u0322M\3\2\2\2\u0323\u0321\3\2\2\2\u0324\u032d\5P)\2")
        buf.write("\u0325\u032d\5~@\2\u0326\u032d\5\u0082B\2\u0327\u032d")
        buf.write("\5\u0088E\2\u0328\u032d\5\u009cO\2\u0329\u032d\5\u008e")
        buf.write("H\2\u032a\u032d\5\u0090I\2\u032b\u032d\5\u00a8U\2\u032c")
        buf.write("\u0324\3\2\2\2\u032c\u0325\3\2\2\2\u032c\u0326\3\2\2\2")
        buf.write("\u032c\u0327\3\2\2\2\u032c\u0328\3\2\2\2\u032c\u0329\3")
        buf.write("\2\2\2\u032c\u032a\3\2\2\2\u032c\u032b\3\2\2\2\u032dO")
        buf.write("\3\2\2\2\u032e\u0332\5R*\2\u032f\u0331\5T+\2\u0330\u032f")
        buf.write("\3\2\2\2\u0331\u0334\3\2\2\2\u0332\u0330\3\2\2\2\u0332")
        buf.write("\u0333\3\2\2\2\u0333\u0335\3\2\2\2\u0334\u0332\3\2\2\2")
        buf.write("\u0335\u0336\5|?\2\u0336Q\3\2\2\2\u0337\u033b\5V,\2\u0338")
        buf.write("\u033b\5^\60\2\u0339\u033b\5b\62\2\u033a\u0337\3\2\2\2")
        buf.write("\u033a\u0338\3\2\2\2\u033a\u0339\3\2\2\2\u033bS\3\2\2")
        buf.write("\2\u033c\u0342\5R*\2\u033d\u0342\5p9\2\u033e\u0342\5r")
        buf.write(":\2\u033f\u0342\5x=\2\u0340\u0342\5n8\2\u0341\u033c\3")
        buf.write("\2\2\2\u0341\u033d\3\2\2\2\u0341\u033e\3\2\2\2\u0341\u033f")
        buf.write("\3\2\2\2\u0341\u0340\3\2\2\2\u0342U\3\2\2\2\u0343\u0344")
        buf.write("\7d\2\2\u0344\u0349\5X-\2\u0345\u0346\7 \2\2\u0346\u0348")
        buf.write("\5X-\2\u0347\u0345\3\2\2\2\u0348\u034b\3\2\2\2\u0349\u0347")
        buf.write("\3\2\2\2\u0349\u034a\3\2\2\2\u034aW\3\2\2\2\u034b\u0349")
        buf.write("\3\2\2\2\u034c\u034d\7.\2\2\u034d\u034f\5\u0106\u0084")
        buf.write("\2\u034e\u0350\5\u0176\u00bc\2\u034f\u034e\3\2\2\2\u034f")
        buf.write("\u0350\3\2\2\2\u0350\u0352\3\2\2\2\u0351\u0353\5Z.\2\u0352")
        buf.write("\u0351\3\2\2\2\u0352\u0353\3\2\2\2\u0353\u0355\3\2\2\2")
        buf.write("\u0354\u0356\5\\/\2\u0355\u0354\3\2\2\2\u0355\u0356\3")
        buf.write("\2\2\2\u0356\u0357\3\2\2\2\u0357\u0358\7m\2\2\u0358\u0359")
        buf.write("\5N(\2\u0359Y\3\2\2\2\u035a\u035b\7\67\2\2\u035b\u035c")
        buf.write("\7Z\2\2\u035c[\3\2\2\2\u035d\u035e\7>\2\2\u035e\u035f")
        buf.write("\7.\2\2\u035f\u0360\5\u0106\u0084\2\u0360]\3\2\2\2\u0361")
        buf.write("\u0362\7v\2\2\u0362\u0367\5`\61\2\u0363\u0364\7 \2\2\u0364")
        buf.write("\u0366\5`\61\2\u0365\u0363\3\2\2\2\u0366\u0369\3\2\2\2")
        buf.write("\u0367\u0365\3\2\2\2\u0367\u0368\3\2\2\2\u0368_\3\2\2")
        buf.write("\2\u0369\u0367\3\2\2\2\u036a\u036b\7.\2\2\u036b\u036d")
        buf.write("\5\u0106\u0084\2\u036c\u036e\5\u0176\u00bc\2\u036d\u036c")
        buf.write("\3\2\2\2\u036d\u036e\3\2\2\2\u036e\u036f\3\2\2\2\u036f")
        buf.write("\u0370\7$\2\2\u0370\u0371\5N(\2\u0371a\3\2\2\2\u0372\u0375")
        buf.write("\7d\2\2\u0373\u0376\5d\63\2\u0374\u0376\5f\64\2\u0375")
        buf.write("\u0373\3\2\2\2\u0375\u0374\3\2\2\2\u0376c\3\2\2\2\u0377")
        buf.write("\u0378\7\u00a1\2\2\u0378\u0379\7\u00ac\2\2\u0379\u037a")
        buf.write("\7.\2\2\u037a\u037c\5\u01c8\u00e5\2\u037b\u037d\5\u0176")
        buf.write("\u00bc\2\u037c\u037b\3\2\2\2\u037c\u037d\3\2\2\2\u037d")
        buf.write("\u037e\3\2\2\2\u037e\u037f\7m\2\2\u037f\u0380\5N(\2\u0380")
        buf.write("\u0382\5h\65\2\u0381\u0383\5j\66\2\u0382\u0381\3\2\2\2")
        buf.write("\u0382\u0383\3\2\2\2\u0383e\3\2\2\2\u0384\u0385\7\u0095")
        buf.write("\2\2\u0385\u0386\7\u00ac\2\2\u0386\u0387\7.\2\2\u0387")
        buf.write("\u0389\5\u01c8\u00e5\2\u0388\u038a\5\u0176\u00bc\2\u0389")
        buf.write("\u0388\3\2\2\2\u0389\u038a\3\2\2\2\u038a\u038b\3\2\2\2")
        buf.write("\u038b\u038c\7m\2\2\u038c\u038d\5N(\2\u038d\u038e\5h\65")
        buf.write("\2\u038e\u038f\5j\66\2\u038fg\3\2\2\2\u0390\u0391\7\u0098")
        buf.write("\2\2\u0391\u0392\5l\67\2\u0392\u0393\7\u00aa\2\2\u0393")
        buf.write("\u0394\5N(\2\u0394i\3\2\2\2\u0395\u0397\7\u0083\2\2\u0396")
        buf.write("\u0395\3\2\2\2\u0396\u0397\3\2\2\2\u0397\u0398\3\2\2\2")
        buf.write("\u0398\u0399\7]\2\2\u0399\u039a\5l\67\2\u039a\u039b\7")
        buf.write("\u00aa\2\2\u039b\u039c\5N(\2\u039ck\3\2\2\2\u039d\u039e")
        buf.write("\7.\2\2\u039e\u03a0\5\u01c6\u00e4\2\u039f\u039d\3\2\2")
        buf.write("\2\u039f\u03a0\3\2\2\2\u03a0\u03a2\3\2\2\2\u03a1\u03a3")
        buf.write("\5\\/\2\u03a2\u03a1\3\2\2\2\u03a2\u03a3\3\2\2\2\u03a3")
        buf.write("\u03a7\3\2\2\2\u03a4\u03a5\7\u008d\2\2\u03a5\u03a6\7.")
        buf.write("\2\2\u03a6\u03a8\5\u01c6\u00e4\2\u03a7\u03a4\3\2\2\2\u03a7")
        buf.write("\u03a8\3\2\2\2\u03a8\u03ac\3\2\2\2\u03a9\u03aa\7}\2\2")
        buf.write("\u03aa\u03ab\7.\2\2\u03ab\u03ad\5\u01c6\u00e4\2\u03ac")
        buf.write("\u03a9\3\2\2\2\u03ac\u03ad\3\2\2\2\u03adm\3\2\2\2\u03ae")
        buf.write("\u03af\7N\2\2\u03af\u03b0\7.\2\2\u03b0\u03b1\5\u0106\u0084")
        buf.write("\2\u03b1o\3\2\2\2\u03b2\u03b3\7\u00ab\2\2\u03b3\u03b4")
        buf.write("\5N(\2\u03b4q\3\2\2\2\u03b5\u03b6\7h\2\2\u03b6\u03b7\7")
        buf.write("C\2\2\u03b7\u03b8\5t;\2\u03b8s\3\2\2\2\u03b9\u03be\5v")
        buf.write("<\2\u03ba\u03bb\7 \2\2\u03bb\u03bd\5v<\2\u03bc\u03ba\3")
        buf.write("\2\2\2\u03bd\u03c0\3\2\2\2\u03be\u03bc\3\2\2\2\u03be\u03bf")
        buf.write("\3\2\2\2\u03bfu\3\2\2\2\u03c0\u03be\3\2\2\2\u03c1\u03c2")
        buf.write("\7.\2\2\u03c2\u03c8\5\u0106\u0084\2\u03c3\u03c5\5\u0176")
        buf.write("\u00bc\2\u03c4\u03c3\3\2\2\2\u03c4\u03c5\3\2\2\2\u03c5")
        buf.write("\u03c6\3\2\2\2\u03c6\u03c7\7$\2\2\u03c7\u03c9\5N(\2\u03c8")
        buf.write("\u03c4\3\2\2\2\u03c8\u03c9\3\2\2\2\u03c9\u03cc\3\2\2\2")
        buf.write("\u03ca\u03cb\7I\2\2\u03cb\u03cd\5\u01d4\u00eb\2\u03cc")
        buf.write("\u03ca\3\2\2\2\u03cc\u03cd\3\2\2\2\u03cdw\3\2\2\2\u03ce")
        buf.write("\u03d0\7\u0097\2\2\u03cf\u03ce\3\2\2\2\u03cf\u03d0\3\2")
        buf.write("\2\2\u03d0\u03d1\3\2\2\2\u03d1\u03d2\7\u0086\2\2\u03d2")
        buf.write("\u03d3\7C\2\2\u03d3\u03d8\5z>\2\u03d4\u03d5\7 \2\2\u03d5")
        buf.write("\u03d7\5z>\2\u03d6\u03d4\3\2\2\2\u03d7\u03da\3\2\2\2\u03d8")
        buf.write("\u03d6\3\2\2\2\u03d8\u03d9\3\2\2\2\u03d9y\3\2\2\2\u03da")
        buf.write("\u03d8\3\2\2\2\u03db\u03dd\5N(\2\u03dc\u03de\t\b\2\2\u03dd")
        buf.write("\u03dc\3\2\2\2\u03dd\u03de\3\2\2\2\u03de\u03e1\3\2\2\2")
        buf.write("\u03df\u03e0\7Z\2\2\u03e0\u03e2\t\5\2\2\u03e1\u03df\3")
        buf.write("\2\2\2\u03e1\u03e2\3\2\2\2\u03e2\u03e5\3\2\2\2\u03e3\u03e4")
        buf.write("\7I\2\2\u03e4\u03e6\5\u01d4\u00eb\2\u03e5\u03e3\3\2\2")
        buf.write("\2\u03e5\u03e6\3\2\2\2\u03e6{\3\2\2\2\u03e7\u03e8\7\u008f")
        buf.write("\2\2\u03e8\u03e9\5N(\2\u03e9}\3\2\2\2\u03ea\u03eb\t\t")
        buf.write("\2\2\u03eb\u03f0\5\u0080A\2\u03ec\u03ed\7 \2\2\u03ed\u03ef")
        buf.write("\5\u0080A\2\u03ee\u03ec\3\2\2\2\u03ef\u03f2\3\2\2\2\u03f0")
        buf.write("\u03ee\3\2\2\2\u03f0\u03f1\3\2\2\2\u03f1\u03f3\3\2\2\2")
        buf.write("\u03f2\u03f0\3\2\2\2\u03f3\u03f4\7\u0090\2\2\u03f4\u03f5")
        buf.write("\5N(\2\u03f5\177\3\2\2\2\u03f6\u03f7\7.\2\2\u03f7\u03f9")
        buf.write("\5\u0106\u0084\2\u03f8\u03fa\5\u0176\u00bc\2\u03f9\u03f8")
        buf.write("\3\2\2\2\u03f9\u03fa\3\2\2\2\u03fa\u03fb\3\2\2\2\u03fb")
        buf.write("\u03fc\7m\2\2\u03fc\u03fd\5N(\2\u03fd\u0081\3\2\2\2\u03fe")
        buf.write("\u03ff\7\u009b\2\2\u03ff\u0400\7\27\2\2\u0400\u0401\5")
        buf.write("L\'\2\u0401\u0403\7\30\2\2\u0402\u0404\5\u0084C\2\u0403")
        buf.write("\u0402\3\2\2\2\u0404\u0405\3\2\2\2\u0405\u0403\3\2\2\2")
        buf.write("\u0405\u0406\3\2\2\2\u0406\u0407\3\2\2\2\u0407\u0408\7")
        buf.write("P\2\2\u0408\u0409\7\u008f\2\2\u0409\u040a\5N(\2\u040a")
        buf.write("\u0083\3\2\2\2\u040b\u040c\7D\2\2\u040c\u040e\5\u0086")
        buf.write("D\2\u040d\u040b\3\2\2\2\u040e\u040f\3\2\2\2\u040f\u040d")
        buf.write("\3\2\2\2\u040f\u0410\3\2\2\2\u0410\u0411\3\2\2\2\u0411")
        buf.write("\u0412\7\u008f\2\2\u0412\u0413\5N(\2\u0413\u0085\3\2\2")
        buf.write("\2\u0414\u0415\5N(\2\u0415\u0087\3\2\2\2\u0416\u0417\7")
        buf.write("\u00a3\2\2\u0417\u0418\7\27\2\2\u0418\u0419\5L\'\2\u0419")
        buf.write("\u041b\7\30\2\2\u041a\u041c\5\u008aF\2\u041b\u041a\3\2")
        buf.write("\2\2\u041c\u041d\3\2\2\2\u041d\u041b\3\2\2\2\u041d\u041e")
        buf.write("\3\2\2\2\u041e\u041f\3\2\2\2\u041f\u0422\7P\2\2\u0420")
        buf.write("\u0421\7.\2\2\u0421\u0423\5\u0106\u0084\2\u0422\u0420")
        buf.write("\3\2\2\2\u0422\u0423\3\2\2\2\u0423\u0424\3\2\2\2\u0424")
        buf.write("\u0425\7\u008f\2\2\u0425\u0426\5N(\2\u0426\u0089\3\2\2")
        buf.write("\2\u0427\u042c\7D\2\2\u0428\u0429\7.\2\2\u0429\u042a\5")
        buf.write("\u0106\u0084\2\u042a\u042b\7<\2\2\u042b\u042d\3\2\2\2")
        buf.write("\u042c\u0428\3\2\2\2\u042c\u042d\3\2\2\2\u042d\u042e\3")
        buf.write("\2\2\2\u042e\u042f\5\u008cG\2\u042f\u0430\7\u008f\2\2")
        buf.write("\u0430\u0431\5N(\2\u0431\u008b\3\2\2\2\u0432\u0437\5\u0178")
        buf.write("\u00bd\2\u0433\u0434\7)\2\2\u0434\u0436\5\u0178\u00bd")
        buf.write("\2\u0435\u0433\3\2\2\2\u0436\u0439\3\2\2\2\u0437\u0435")
        buf.write("\3\2\2\2\u0437\u0438\3\2\2\2\u0438\u008d\3\2\2\2\u0439")
        buf.write("\u0437\3\2\2\2\u043a\u043b\7k\2\2\u043b\u043c\7\27\2\2")
        buf.write("\u043c\u043d\5L\'\2\u043d\u043e\7\30\2\2\u043e\u043f\7")
        buf.write("\u009d\2\2\u043f\u0440\5N(\2\u0440\u0441\7Y\2\2\u0441")
        buf.write("\u0442\5N(\2\u0442\u008f\3\2\2\2\u0443\u0445\5\u0092J")
        buf.write("\2\u0444\u0446\5\u0096L\2\u0445\u0444\3\2\2\2\u0446\u0447")
        buf.write("\3\2\2\2\u0447\u0445\3\2\2\2\u0447\u0448\3\2\2\2\u0448")
        buf.write("\u0091\3\2\2\2\u0449\u044a\7\u00a0\2\2\u044a\u044b\5\u0094")
        buf.write("K\2\u044b\u0093\3\2\2\2\u044c\u044d\5\u0098M\2\u044d\u0095")
        buf.write("\3\2\2\2\u044e\u0455\7G\2\2\u044f\u0456\5\u009aN\2\u0450")
        buf.write("\u0451\7\27\2\2\u0451\u0452\7.\2\2\u0452\u0453\5\u0106")
        buf.write("\u0084\2\u0453\u0454\7\30\2\2\u0454\u0456\3\2\2\2\u0455")
        buf.write("\u044f\3\2\2\2\u0455\u0450\3\2\2\2\u0456\u0457\3\2\2\2")
        buf.write("\u0457\u0458\5\u0098M\2\u0458\u0097\3\2\2\2\u0459\u045b")
        buf.write("\7\33\2\2\u045a\u045c\5L\'\2\u045b\u045a\3\2\2\2\u045b")
        buf.write("\u045c\3\2\2\2\u045c\u045d\3\2\2\2\u045d\u045e\7\34\2")
        buf.write("\2\u045e\u0099\3\2\2\2\u045f\u0464\5\u00ecw\2\u0460\u0461")
        buf.write("\7)\2\2\u0461\u0463\5\u00ecw\2\u0462\u0460\3\2\2\2\u0463")
        buf.write("\u0466\3\2\2\2\u0464\u0462\3\2\2\2\u0464\u0465\3\2\2\2")
        buf.write("\u0465\u009b\3\2\2\2\u0466\u0464\3\2\2\2\u0467\u046d\7")
        buf.write("\u00a6\2\2\u0468\u046e\5\u009eP\2\u0469\u046e\5\u00a0")
        buf.write("Q\2\u046a\u046e\5\u00a2R\2\u046b\u046e\5\u00a4S\2\u046c")
        buf.write("\u046e\5\u00a6T\2\u046d\u0468\3\2\2\2\u046d\u0469\3\2")
        buf.write("\2\2\u046d\u046a\3\2\2\2\u046d\u046b\3\2\2\2\u046d\u046c")
        buf.write("\3\2\2\2\u046e\u009d\3\2\2\2\u046f\u0470\7\u00b3\2\2\u0470")
        buf.write("\u0471\5L\'\2\u0471\u0472\7\u00b4\2\2\u0472\u0473\5N(")
        buf.write("\2\u0473\u009f\3\2\2\2\u0474\u0475\7\u00b5\2\2\u0475\u0476")
        buf.write("\5L\'\2\u0476\u0477\7\u00b4\2\2\u0477\u0478\5N(\2\u0478")
        buf.write("\u00a1\3\2\2\2\u0479\u047a\7\u00b6\2\2\u047a\u047b\5N")
        buf.write("(\2\u047b\u047c\t\n\2\2\u047c\u047d\5N(\2\u047d\u00a3")
        buf.write("\3\2\2\2\u047e\u047f\7\u00b8\2\2\u047f\u0480\5N(\2\u0480")
        buf.write("\u00a5\3\2\2\2\u0481\u0482\7\u00b9\2\2\u0482\u0483\5N")
        buf.write("(\2\u0483\u0484\7<\2\2\u0484\u0485\5N(\2\u0485\u00a7\3")
        buf.write("\2\2\2\u0486\u048b\5\u00aaV\2\u0487\u0488\7\u0085\2\2")
        buf.write("\u0488\u048a\5\u00aaV\2\u0489\u0487\3\2\2\2\u048a\u048d")
        buf.write("\3\2\2\2\u048b\u0489\3\2\2\2\u048b\u048c\3\2\2\2\u048c")
        buf.write("\u00a9\3\2\2\2\u048d\u048b\3\2\2\2\u048e\u0493\5\u00ac")
        buf.write("W\2\u048f\u0490\7:\2\2\u0490\u0492\5\u00acW\2\u0491\u048f")
        buf.write("\3\2\2\2\u0492\u0495\3\2\2\2\u0493\u0491\3\2\2\2\u0493")
        buf.write("\u0494\3\2\2\2\u0494\u00ab\3\2\2\2\u0495\u0493\3\2\2\2")
        buf.write("\u0496\u049e\5\u00aeX\2\u0497\u049b\5\u00caf\2\u0498\u049b")
        buf.write("\5\u00c8e\2\u0499\u049b\5\u00ccg\2\u049a\u0497\3\2\2\2")
        buf.write("\u049a\u0498\3\2\2\2\u049a\u0499\3\2\2\2\u049b\u049c\3")
        buf.write("\2\2\2\u049c\u049d\5\u00aeX\2\u049d\u049f\3\2\2\2\u049e")
        buf.write("\u049a\3\2\2\2\u049e\u049f\3\2\2\2\u049f\u00ad\3\2\2\2")
        buf.write("\u04a0\u04a5\5\u00b0Y\2\u04a1\u04a2\7\65\2\2\u04a2\u04a4")
        buf.write("\5\u00b0Y\2\u04a3\u04a1\3\2\2\2\u04a4\u04a7\3\2\2\2\u04a5")
        buf.write("\u04a3\3\2\2\2\u04a5\u04a6\3\2\2\2\u04a6\u00af\3\2\2\2")
        buf.write("\u04a7\u04a5\3\2\2\2\u04a8\u04ab\5\u00b2Z\2\u04a9\u04aa")
        buf.write("\7\u009e\2\2\u04aa\u04ac\5\u00b2Z\2\u04ab\u04a9\3\2\2")
        buf.write("\2\u04ab\u04ac\3\2\2\2\u04ac\u00b1\3\2\2\2\u04ad\u04b2")
        buf.write("\5\u00b4[\2\u04ae\u04af\t\13\2\2\u04af\u04b1\5\u00b4[")
        buf.write("\2\u04b0\u04ae\3\2\2\2\u04b1\u04b4\3\2\2\2\u04b2\u04b0")
        buf.write("\3\2\2\2\u04b2\u04b3\3\2\2\2\u04b3\u00b3\3\2\2\2\u04b4")
        buf.write("\u04b2\3\2\2\2\u04b5\u04ba\5\u00b6\\\2\u04b6\u04b7\t\f")
        buf.write("\2\2\u04b7\u04b9\5\u00b6\\\2\u04b8\u04b6\3\2\2\2\u04b9")
        buf.write("\u04bc\3\2\2\2\u04ba\u04b8\3\2\2\2\u04ba\u04bb\3\2\2\2")
        buf.write("\u04bb\u00b5\3\2\2\2\u04bc\u04ba\3\2\2\2\u04bd\u04c2\5")
        buf.write("\u00b8]\2\u04be\u04bf\t\r\2\2\u04bf\u04c1\5\u00b8]\2\u04c0")
        buf.write("\u04be\3\2\2\2\u04c1\u04c4\3\2\2\2\u04c2\u04c0\3\2\2\2")
        buf.write("\u04c2\u04c3\3\2\2\2\u04c3\u00b7\3\2\2\2\u04c4\u04c2\3")
        buf.write("\2\2\2\u04c5\u04ca\5\u00ba^\2\u04c6\u04c7\t\16\2\2\u04c7")
        buf.write("\u04c9\5\u00ba^\2\u04c8\u04c6\3\2\2\2\u04c9\u04cc\3\2")
        buf.write("\2\2\u04ca\u04c8\3\2\2\2\u04ca\u04cb\3\2\2\2\u04cb\u00b9")
        buf.write("\3\2\2\2\u04cc\u04ca\3\2\2\2\u04cd\u04d1\5\u00bc_\2\u04ce")
        buf.write("\u04cf\7o\2\2\u04cf\u04d0\7\u0082\2\2\u04d0\u04d2\5\u0178")
        buf.write("\u00bd\2\u04d1\u04ce\3\2\2\2\u04d1\u04d2\3\2\2\2\u04d2")
        buf.write("\u00bb\3\2\2\2\u04d3\u04d7\5\u00be`\2\u04d4\u04d5\7\u009f")
        buf.write("\2\2\u04d5\u04d6\7<\2\2\u04d6\u04d8\5\u0178\u00bd\2\u04d7")
        buf.write("\u04d4\3\2\2\2\u04d7\u04d8\3\2\2\2\u04d8\u00bd\3\2\2\2")
        buf.write("\u04d9\u04dd\5\u00c0a\2\u04da\u04db\7F\2\2\u04db\u04dc")
        buf.write("\7<\2\2\u04dc\u04de\5\u0174\u00bb\2\u04dd\u04da\3\2\2")
        buf.write("\2\u04dd\u04de\3\2\2\2\u04de\u00bf\3\2\2\2\u04df\u04e3")
        buf.write("\5\u00c2b\2\u04e0\u04e1\7E\2\2\u04e1\u04e2\7<\2\2\u04e2")
        buf.write("\u04e4\5\u0174\u00bb\2\u04e3\u04e0\3\2\2\2\u04e3\u04e4")
        buf.write("\3\2\2\2\u04e4\u00c1\3\2\2\2\u04e5\u04ec\5\u00c4c\2\u04e6")
        buf.write("\u04e7\7\63\2\2\u04e7\u04e8\5\u00fc\177\2\u04e8\u04e9")
        buf.write("\5\u00f2z\2\u04e9\u04eb\3\2\2\2\u04ea\u04e6\3\2\2\2\u04eb")
        buf.write("\u04ee\3\2\2\2\u04ec\u04ea\3\2\2\2\u04ec\u04ed\3\2\2\2")
        buf.write("\u04ed\u00c3\3\2\2\2\u04ee\u04ec\3\2\2\2\u04ef\u04f1\t")
        buf.write("\13\2\2\u04f0\u04ef\3\2\2\2\u04f1\u04f4\3\2\2\2\u04f2")
        buf.write("\u04f0\3\2\2\2\u04f2\u04f3\3\2\2\2\u04f3\u04f5\3\2\2\2")
        buf.write("\u04f4\u04f2\3\2\2\2\u04f5\u04f6\5\u00c6d\2\u04f6\u00c5")
        buf.write("\3\2\2\2\u04f7\u04fb\5\u00ceh\2\u04f8\u04fb\5\u00d2j\2")
        buf.write("\u04f9\u04fb\5\u00d4k\2\u04fa\u04f7\3\2\2\2\u04fa\u04f8")
        buf.write("\3\2\2\2\u04fa\u04f9\3\2\2\2\u04fb\u00c7\3\2\2\2\u04fc")
        buf.write("\u0505\7\25\2\2\u04fd\u0505\7\26\2\2\u04fe\u0505\7*\2")
        buf.write("\2\u04ff\u0500\7*\2\2\u0500\u0505\7\25\2\2\u0501\u0505")
        buf.write("\7+\2\2\u0502\u0503\7+\2\2\u0503\u0505\7\25\2\2\u0504")
        buf.write("\u04fc\3\2\2\2\u0504\u04fd\3\2\2\2\u0504\u04fe\3\2\2\2")
        buf.write("\u0504\u04ff\3\2\2\2\u0504\u0501\3\2\2\2\u0504\u0502\3")
        buf.write("\2\2\2\u0505\u00c9\3\2\2\2\u0506\u0507\t\17\2\2\u0507")
        buf.write("\u00cb\3\2\2\2\u0508\u050e\7q\2\2\u0509\u050a\7*\2\2\u050a")
        buf.write("\u050e\7*\2\2\u050b\u050c\7+\2\2\u050c\u050e\7+\2\2\u050d")
        buf.write("\u0508\3\2\2\2\u050d\u0509\3\2\2\2\u050d\u050b\3\2\2\2")
        buf.write("\u050e\u00cd\3\2\2\2\u050f\u0513\7\u00a7\2\2\u0510\u0514")
        buf.write("\5\u00d0i\2\u0511\u0512\t\20\2\2\u0512\u0514\5\u01a2\u00d2")
        buf.write("\2\u0513\u0510\3\2\2\2\u0513\u0511\3\2\2\2\u0513\u0514")
        buf.write("\3\2\2\2\u0514\u0515\3\2\2\2\u0515\u0516\5\u0098M\2\u0516")
        buf.write("\u00cf\3\2\2\2\u0517\u0518\t\21\2\2\u0518\u00d1\3\2\2")
        buf.write("\2\u0519\u051b\7\23\2\2\u051a\u0519\3\2\2\2\u051b\u051c")
        buf.write("\3\2\2\2\u051c\u051a\3\2\2\2\u051c\u051d\3\2\2\2\u051d")
        buf.write("\u051e\3\2\2\2\u051e\u051f\7\33\2\2\u051f\u0520\5L\'\2")
        buf.write("\u0520\u0521\7\34\2\2\u0521\u00d3\3\2\2\2\u0522\u0527")
        buf.write("\5\u00d6l\2\u0523\u0524\7\60\2\2\u0524\u0526\5\u00d6l")
        buf.write("\2\u0525\u0523\3\2\2\2\u0526\u0529\3\2\2\2\u0527\u0525")
        buf.write("\3\2\2\2\u0527\u0528\3\2\2\2\u0528\u00d5\3\2\2\2\u0529")
        buf.write("\u0527\3\2\2\2\u052a\u052c\7&\2\2\u052b\u052d\5\u00d8")
        buf.write("m\2\u052c\u052b\3\2\2\2\u052c\u052d\3\2\2\2\u052d\u0532")
        buf.write("\3\2\2\2\u052e\u052f\7\'\2\2\u052f\u0532\5\u00d8m\2\u0530")
        buf.write("\u0532\5\u00d8m\2\u0531\u052a\3\2\2\2\u0531\u052e\3\2")
        buf.write("\2\2\u0531\u0530\3\2\2\2\u0532\u00d7\3\2\2\2\u0533\u0538")
        buf.write("\5\u00dan\2\u0534\u0535\t\22\2\2\u0535\u0537\5\u00dan")
        buf.write("\2\u0536\u0534\3\2\2\2\u0537\u053a\3\2\2\2\u0538\u0536")
        buf.write("\3\2\2\2\u0538\u0539\3\2\2\2\u0539\u00d9\3\2\2\2\u053a")
        buf.write("\u0538\3\2\2\2\u053b\u053e\5\u00f0y\2\u053c\u053e\5\u00dc")
        buf.write("o\2\u053d\u053b\3\2\2\2\u053d\u053c\3\2\2\2\u053e\u00db")
        buf.write("\3\2\2\2\u053f\u0542\5\u00e4s\2\u0540\u0542\5\u00dep\2")
        buf.write("\u0541\u053f\3\2\2\2\u0541\u0540\3\2\2\2\u0542\u0543\3")
        buf.write("\2\2\2\u0543\u0544\5\u00f4{\2\u0544\u00dd\3\2\2\2\u0545")
        buf.write("\u0546\5\u00e0q\2\u0546\u0547\5\u00eav\2\u0547\u054a\3")
        buf.write("\2\2\2\u0548\u054a\5\u00e2r\2\u0549\u0545\3\2\2\2\u0549")
        buf.write("\u0548\3\2\2\2\u054a\u00df\3\2\2\2\u054b\u054c\t\23\2")
        buf.write("\2\u054c\u054d\7#\2\2\u054d\u054e\7#\2\2\u054e\u00e1\3")
        buf.write("\2\2\2\u054f\u0551\7-\2\2\u0550\u054f\3\2\2\2\u0550\u0551")
        buf.write("\3\2\2\2\u0551\u0552\3\2\2\2\u0552\u0553\5\u00eav\2\u0553")
        buf.write("\u00e3\3\2\2\2\u0554\u0555\5\u00e6t\2\u0555\u0556\5\u00ea")
        buf.write("v\2\u0556\u0559\3\2\2\2\u0557\u0559\5\u00e8u\2\u0558\u0554")
        buf.write("\3\2\2\2\u0558\u0557\3\2\2\2\u0559\u00e5\3\2\2\2\u055a")
        buf.write("\u055b\t\24\2\2\u055b\u055c\7#\2\2\u055c\u055d\7#\2\2")
        buf.write("\u055d\u00e7\3\2\2\2\u055e\u055f\7\"\2\2\u055f\u00e9\3")
        buf.write("\2\2\2\u0560\u0563\5\u00ecw\2\u0561\u0563\5\u017e\u00c0")
        buf.write("\2\u0562\u0560\3\2\2\2\u0562\u0561\3\2\2\2\u0563\u00eb")
        buf.write("\3\2\2\2\u0564\u0567\5\u01c6\u00e4\2\u0565\u0567\5\u00ee")
        buf.write("x\2\u0566\u0564\3\2\2\2\u0566\u0565\3\2\2\2\u0567\u00ed")
        buf.write("\3\2\2\2\u0568\u056c\7\35\2\2\u0569\u056c\7\u00bc\2\2")
        buf.write("\u056a\u056c\7\u00bd\2\2\u056b\u0568\3\2\2\2\u056b\u0569")
        buf.write("\3\2\2\2\u056b\u056a\3\2\2\2\u056c\u00ef\3\2\2\2\u056d")
        buf.write("\u0573\5\u00fe\u0080\2\u056e\u0572\5\u00f6|\2\u056f\u0572")
        buf.write("\5\u00f2z\2\u0570\u0572\5\u00f8}\2\u0571\u056e\3\2\2\2")
        buf.write("\u0571\u056f\3\2\2\2\u0571\u0570\3\2\2\2\u0572\u0575\3")
        buf.write("\2\2\2\u0573\u0571\3\2\2\2\u0573\u0574\3\2\2\2\u0574\u00f1")
        buf.write("\3\2\2\2\u0575\u0573\3\2\2\2\u0576\u057f\7\27\2\2\u0577")
        buf.write("\u057c\5\u0112\u008a\2\u0578\u0579\7 \2\2\u0579\u057b")
        buf.write("\5\u0112\u008a\2\u057a\u0578\3\2\2\2\u057b\u057e\3\2\2")
        buf.write("\2\u057c\u057a\3\2\2\2\u057c\u057d\3\2\2\2\u057d\u0580")
        buf.write("\3\2\2\2\u057e\u057c\3\2\2\2\u057f\u0577\3\2\2\2\u057f")
        buf.write("\u0580\3\2\2\2\u0580\u0581\3\2\2\2\u0581\u0582\7\30\2")
        buf.write("\2\u0582\u00f3\3\2\2\2\u0583\u0585\5\u00f6|\2\u0584\u0583")
        buf.write("\3\2\2\2\u0585\u0588\3\2\2\2\u0586\u0584\3\2\2\2\u0586")
        buf.write("\u0587\3\2\2\2\u0587\u00f5\3\2\2\2\u0588\u0586\3\2\2\2")
        buf.write("\u0589\u058a\7\31\2\2\u058a\u058b\5L\'\2\u058b\u058c\7")
        buf.write("\32\2\2\u058c\u00f7\3\2\2\2\u058d\u058e\7,\2\2\u058e\u058f")
        buf.write("\5\u00fa~\2\u058f\u00f9\3\2\2\2\u0590\u0595\5\u01ca\u00e6")
        buf.write("\2\u0591\u0595\7\7\2\2\u0592\u0595\5\u0108\u0085\2\u0593")
        buf.write("\u0595\7\35\2\2\u0594\u0590\3\2\2\2\u0594\u0591\3\2\2")
        buf.write("\2\u0594\u0592\3\2\2\2\u0594\u0593\3\2\2\2\u0595\u00fb")
        buf.write("\3\2\2\2\u0596\u059a\5\u01c6\u00e4\2\u0597\u059a\5\u0104")
        buf.write("\u0083\2\u0598\u059a\5\u0108\u0085\2\u0599\u0596\3\2\2")
        buf.write("\2\u0599\u0597\3\2\2\2\u0599\u0598\3\2\2\2\u059a\u00fd")
        buf.write("\3\2\2\2\u059b\u05a9\5\u0100\u0081\2\u059c\u05a9\5\u0104")
        buf.write("\u0083\2\u059d\u05a9\5\u0108\u0085\2\u059e\u05a9\5\u010a")
        buf.write("\u0086\2\u059f\u05a9\5\u0110\u0089\2\u05a0\u05a9\5\u010c")
        buf.write("\u0087\2\u05a1\u05a9\5\u010e\u0088\2\u05a2\u05a9\5\u0114")
        buf.write("\u008b\2\u05a3\u05a9\5\u0152\u00aa\2\u05a4\u05a9\5\u015a")
        buf.write("\u00ae\2\u05a5\u05a9\5\u015e\u00b0\2\u05a6\u05a9\5\u0164")
        buf.write("\u00b3\2\u05a7\u05a9\5\u0172\u00ba\2\u05a8\u059b\3\2\2")
        buf.write("\2\u05a8\u059c\3\2\2\2\u05a8\u059d\3\2\2\2\u05a8\u059e")
        buf.write("\3\2\2\2\u05a8\u059f\3\2\2\2\u05a8\u05a0\3\2\2\2\u05a8")
        buf.write("\u05a1\3\2\2\2\u05a8\u05a2\3\2\2\2\u05a8\u05a3\3\2\2\2")
        buf.write("\u05a8\u05a4\3\2\2\2\u05a8\u05a5\3\2\2\2\u05a8\u05a6\3")
        buf.write("\2\2\2\u05a8\u05a7\3\2\2\2\u05a9\u00ff\3\2\2\2\u05aa\u05ad")
        buf.write("\5\u0102\u0082\2\u05ab\u05ad\5\u01da\u00ee\2\u05ac\u05aa")
        buf.write("\3\2\2\2\u05ac\u05ab\3\2\2\2\u05ad\u0101\3\2\2\2\u05ae")
        buf.write("\u05af\t\25\2\2\u05af\u0103\3\2\2\2\u05b0\u05b1\7.\2\2")
        buf.write("\u05b1\u05b2\5\u01c6\u00e4\2\u05b2\u0105\3\2\2\2\u05b3")
        buf.write("\u05b4\5\u01c6\u00e4\2\u05b4\u0107\3\2\2\2\u05b5\u05b7")
        buf.write("\7\27\2\2\u05b6\u05b8\5L\'\2\u05b7\u05b6\3\2\2\2\u05b7")
        buf.write("\u05b8\3\2\2\2\u05b8\u05b9\3\2\2\2\u05b9\u05ba\7\30\2")
        buf.write("\2\u05ba\u0109\3\2\2\2\u05bb\u05bc\7!\2\2\u05bc\u010b")
        buf.write("\3\2\2\2\u05bd\u05be\7\u0087\2\2\u05be\u05bf\5\u0098M")
        buf.write("\2\u05bf\u010d\3\2\2\2\u05c0\u05c1\7\u00a5\2\2\u05c1\u05c2")
        buf.write("\5\u0098M\2\u05c2\u010f\3\2\2\2\u05c3\u05c4\5\u01c6\u00e4")
        buf.write("\2\u05c4\u05c5\5\u00f2z\2\u05c5\u0111\3\2\2\2\u05c6\u05c9")
        buf.write("\5N(\2\u05c7\u05c9\7,\2\2\u05c8\u05c6\3\2\2\2\u05c8\u05c7")
        buf.write("\3\2\2\2\u05c9\u0113\3\2\2\2\u05ca\u05cd\5\u0116\u008c")
        buf.write("\2\u05cb\u05cd\5\u012c\u0097\2\u05cc\u05ca\3\2\2\2\u05cc")
        buf.write("\u05cb\3\2\2\2\u05cd\u0115\3\2\2\2\u05ce\u05d2\5\u0118")
        buf.write("\u008d\2\u05cf\u05d2\5\u011a\u008e\2\u05d0\u05d2\t\26")
        buf.write("\2\2\u05d1\u05ce\3\2\2\2\u05d1\u05cf\3\2\2\2\u05d1\u05d0")
        buf.write("\3\2\2\2\u05d2\u0117\3\2\2\2\u05d3\u05d4\7*\2\2\u05d4")
        buf.write("\u05d5\5\u01c8\u00e5\2\u05d5\u05d6\5\u011c\u008f\2\u05d6")
        buf.write("\u05da\7+\2\2\u05d7\u05d9\5\u0128\u0095\2\u05d8\u05d7")
        buf.write("\3\2\2\2\u05d9\u05dc\3\2\2\2\u05da\u05d8\3\2\2\2\u05da")
        buf.write("\u05db\3\2\2\2\u05db\u05dd\3\2\2\2\u05dc\u05da\3\2\2\2")
        buf.write("\u05dd\u05de\7*\2\2\u05de\u05df\7&\2\2\u05df\u05e0\5\u01c8")
        buf.write("\u00e5\2\u05e0\u05e1\7+\2\2\u05e1\u0119\3\2\2\2\u05e2")
        buf.write("\u05e3\7*\2\2\u05e3\u05e4\5\u01c8\u00e5\2\u05e4\u05e5")
        buf.write("\5\u011c\u008f\2\u05e5\u05e6\7&\2\2\u05e6\u05e7\7+\2\2")
        buf.write("\u05e7\u011b\3\2\2\2\u05e8\u05e9\5\u01c8\u00e5\2\u05e9")
        buf.write("\u05ea\7\25\2\2\u05ea\u05eb\5\u0122\u0092\2\u05eb\u05ed")
        buf.write("\3\2\2\2\u05ec\u05e8\3\2\2\2\u05ed\u05f0\3\2\2\2\u05ee")
        buf.write("\u05ec\3\2\2\2\u05ee\u05ef\3\2\2\2\u05ef\u011d\3\2\2\2")
        buf.write("\u05f0\u05ee\3\2\2\2\u05f1\u05f8\7\r\2\2\u05f2\u05f7\7")
        buf.write("\13\2\2\u05f3\u05f7\7\f\2\2\u05f4\u05f7\7\3\2\2\u05f5")
        buf.write("\u05f7\5\u0124\u0093\2\u05f6\u05f2\3\2\2\2\u05f6\u05f3")
        buf.write("\3\2\2\2\u05f6\u05f4\3\2\2\2\u05f6\u05f5\3\2\2\2\u05f7")
        buf.write("\u05fa\3\2\2\2\u05f8\u05f6\3\2\2\2\u05f8\u05f9\3\2\2\2")
        buf.write("\u05f9\u05fb\3\2\2\2\u05fa\u05f8\3\2\2\2\u05fb\u05fc\7")
        buf.write("\r\2\2\u05fc\u011f\3\2\2\2\u05fd\u0604\7\16\2\2\u05fe")
        buf.write("\u0603\7\13\2\2\u05ff\u0603\7\f\2\2\u0600\u0603\7\4\2")
        buf.write("\2\u0601\u0603\5\u0126\u0094\2\u0602\u05fe\3\2\2\2\u0602")
        buf.write("\u05ff\3\2\2\2\u0602\u0600\3\2\2\2\u0602\u0601\3\2\2\2")
        buf.write("\u0603\u0606\3\2\2\2\u0604\u0602\3\2\2\2\u0604\u0605\3")
        buf.write("\2\2\2\u0605\u0607\3\2\2\2\u0606\u0604\3\2\2\2\u0607\u0608")
        buf.write("\7\16\2\2\u0608\u0121\3\2\2\2\u0609\u060c\5\u011e\u0090")
        buf.write("\2\u060a\u060c\5\u0120\u0091\2\u060b\u0609\3\2\2\2\u060b")
        buf.write("\u060a\3\2\2\2\u060c\u0123\3\2\2\2\u060d\u060f\7\u00c6")
        buf.write("\2\2\u060e\u060d\3\2\2\2\u060f\u0610\3\2\2\2\u0610\u060e")
        buf.write("\3\2\2\2\u0610\u0611\3\2\2\2\u0611\u061b\3\2\2\2\u0612")
        buf.write("\u061b\7\5\2\2\u0613\u061b\7\6\2\2\u0614\u061b\5\u011e")
        buf.write("\u0090\2\u0615\u0617\7\33\2\2\u0616\u0618\5L\'\2\u0617")
        buf.write("\u0616\3\2\2\2\u0617\u0618\3\2\2\2\u0618\u0619\3\2\2\2")
        buf.write("\u0619\u061b\7\34\2\2\u061a\u060e\3\2\2\2\u061a\u0612")
        buf.write("\3\2\2\2\u061a\u0613\3\2\2\2\u061a\u0614\3\2\2\2\u061a")
        buf.write("\u0615\3\2\2\2\u061b\u0125\3\2\2\2\u061c\u061e\7\u00c6")
        buf.write("\2\2\u061d\u061c\3\2\2\2\u061e\u061f\3\2\2\2\u061f\u061d")
        buf.write("\3\2\2\2\u061f\u0620\3\2\2\2\u0620\u062a\3\2\2\2\u0621")
        buf.write("\u062a\7\5\2\2\u0622\u062a\7\6\2\2\u0623\u062a\5\u0120")
        buf.write("\u0091\2\u0624\u0626\7\33\2\2\u0625\u0627\5L\'\2\u0626")
        buf.write("\u0625\3\2\2\2\u0626\u0627\3\2\2\2\u0627\u0628\3\2\2\2")
        buf.write("\u0628\u062a\7\34\2\2\u0629\u061d\3\2\2\2\u0629\u0621")
        buf.write("\3\2\2\2\u0629\u0622\3\2\2\2\u0629\u0623\3\2\2\2\u0629")
        buf.write("\u0624\3\2\2\2\u062a\u0127\3\2\2\2\u062b\u0632\5\u0116")
        buf.write("\u008c\2\u062c\u0632\5\u012a\u0096\2\u062d\u0632\7\22")
        buf.write("\2\2\u062e\u0632\7\r\2\2\u062f\u0632\7\16\2\2\u0630\u0632")
        buf.write("\5\u01e0\u00f1\2\u0631\u062b\3\2\2\2\u0631\u062c\3\2\2")
        buf.write("\2\u0631\u062d\3\2\2\2\u0631\u062e\3\2\2\2\u0631\u062f")
        buf.write("\3\2\2\2\u0631\u0630\3\2\2\2\u0632\u0129\3\2\2\2\u0633")
        buf.write("\u063d\t\27\2\2\u0634\u0635\7\33\2\2\u0635\u063d\7\33")
        buf.write("\2\2\u0636\u0637\7\34\2\2\u0637\u063d\7\34\2\2\u0638\u0639")
        buf.write("\7\33\2\2\u0639\u063a\5L\'\2\u063a\u063b\7\34\2\2\u063b")
        buf.write("\u063d\3\2\2\2\u063c\u0633\3\2\2\2\u063c\u0634\3\2\2\2")
        buf.write("\u063c\u0636\3\2\2\2\u063c\u0638\3\2\2\2\u063d\u012b\3")
        buf.write("\2\2\2\u063e\u0647\5\u013c\u009f\2\u063f\u0647\5\u013e")
        buf.write("\u00a0\2\u0640\u0647\5\u0142\u00a2\2\u0641\u0647\5\u0144")
        buf.write("\u00a3\2\u0642\u0647\5\u014c\u00a7\2\u0643\u0647\5\u014e")
        buf.write("\u00a8\2\u0644\u0647\5\u0150\u00a9\2\u0645\u0647\5\u012e")
        buf.write("\u0098\2\u0646\u063e\3\2\2\2\u0646\u063f\3\2\2\2\u0646")
        buf.write("\u0640\3\2\2\2\u0646\u0641\3\2\2\2\u0646\u0642\3\2\2\2")
        buf.write("\u0646\u0643\3\2\2\2\u0646\u0644\3\2\2\2\u0646\u0645\3")
        buf.write("\2\2\2\u0647\u012d\3\2\2\2\u0648\u064f\5\u0130\u0099\2")
        buf.write("\u0649\u064f\5\u0132\u009a\2\u064a\u064f\5\u0134\u009b")
        buf.write("\2\u064b\u064f\5\u0136\u009c\2\u064c\u064f\5\u0138\u009d")
        buf.write("\2\u064d\u064f\5\u013a\u009e\2\u064e\u0648\3\2\2\2\u064e")
        buf.write("\u0649\3\2\2\2\u064e\u064a\3\2\2\2\u064e\u064b\3\2\2\2")
        buf.write("\u064e\u064c\3\2\2\2\u064e\u064d\3\2\2\2\u064f\u012f\3")
        buf.write("\2\2\2\u0650\u0651\7\u00ae\2\2\u0651\u0652\5\u0140\u00a1")
        buf.write("\2\u0652\u0131\3\2\2\2\u0653\u0654\7\u00b2\2\2\u0654\u0662")
        buf.write("\7\33\2\2\u0655\u0656\5N(\2\u0656\u0657\7#\2\2\u0657\u065f")
        buf.write("\5N(\2\u0658\u0659\7 \2\2\u0659\u065a\5N(\2\u065a\u065b")
        buf.write("\7#\2\2\u065b\u065c\5N(\2\u065c\u065e\3\2\2\2\u065d\u0658")
        buf.write("\3\2\2\2\u065e\u0661\3\2\2\2\u065f\u065d\3\2\2\2\u065f")
        buf.write("\u0660\3\2\2\2\u0660\u0663\3\2\2\2\u0661\u065f\3\2\2\2")
        buf.write("\u0662\u0655\3\2\2\2\u0662\u0663\3\2\2\2\u0663\u0664\3")
        buf.write("\2\2\2\u0664\u0665\7\34\2\2\u0665\u0133\3\2\2\2\u0666")
        buf.write("\u0667\7\u00b1\2\2\u0667\u0668\5\u0140\u00a1\2\u0668\u0135")
        buf.write("\3\2\2\2\u0669\u066a\7\u00af\2\2\u066a\u066b\7\33\2\2")
        buf.write("\u066b\u066c\5N(\2\u066c\u066d\7\34\2\2\u066d\u0137\3")
        buf.write("\2\2\2\u066e\u066f\7\u00b0\2\2\u066f\u0670\7\33\2\2\u0670")
        buf.write("\u0671\7\34\2\2\u0671\u0139\3\2\2\2\u0672\u0673\7B\2\2")
        buf.write("\u0673\u0674\5\u0140\u00a1\2\u0674\u013b\3\2\2\2\u0675")
        buf.write("\u0676\7V\2\2\u0676\u0677\5\u0098M\2\u0677\u013d\3\2\2")
        buf.write("\2\u0678\u067e\7X\2\2\u0679\u067f\5\u01c6\u00e4\2\u067a")
        buf.write("\u067b\7\33\2\2\u067b\u067c\5L\'\2\u067c\u067d\7\34\2")
        buf.write("\2\u067d\u067f\3\2\2\2\u067e\u0679\3\2\2\2\u067e\u067a")
        buf.write("\3\2\2\2\u067f\u0680\3\2\2\2\u0680\u0681\5\u0140\u00a1")
        buf.write("\2\u0681\u013f\3\2\2\2\u0682\u0683\5\u0098M\2\u0683\u0141")
        buf.write("\3\2\2\2\u0684\u068a\7?\2\2\u0685\u068b\5\u01c6\u00e4")
        buf.write("\2\u0686\u0687\7\33\2\2\u0687\u0688\5L\'\2\u0688\u0689")
        buf.write("\7\34\2\2\u0689\u068b\3\2\2\2\u068a\u0685\3\2\2\2\u068a")
        buf.write("\u0686\3\2\2\2\u068b\u068c\3\2\2\2\u068c\u068d\5\u0098")
        buf.write("M\2\u068d\u0143\3\2\2\2\u068e\u0691\7{\2\2\u068f\u0692")
        buf.write("\5\u0146\u00a4\2\u0690\u0692\5\u0148\u00a5\2\u0691\u068f")
        buf.write("\3\2\2\2\u0691\u0690\3\2\2\2\u0692\u0693\3\2\2\2\u0693")
        buf.write("\u0694\5\u014a\u00a6\2\u0694\u0145\3\2\2\2\u0695\u0696")
        buf.write("\5\u01ca\u00e6\2\u0696\u0147\3\2\2\2\u0697\u0698\5\u0098")
        buf.write("M\2\u0698\u0149\3\2\2\2\u0699\u069a\5\u0098M\2\u069a\u014b")
        buf.write("\3\2\2\2\u069b\u069c\7\u009c\2\2\u069c\u069d\5\u0098M")
        buf.write("\2\u069d\u014d\3\2\2\2\u069e\u069f\7J\2\2\u069f\u06a0")
        buf.write("\5\u0098M\2\u06a0\u014f\3\2\2\2\u06a1\u06a7\7\u008e\2")
        buf.write("\2\u06a2\u06a8\5\u01ca\u00e6\2\u06a3\u06a4\7\33\2\2\u06a4")
        buf.write("\u06a5\5L\'\2\u06a5\u06a6\7\34\2\2\u06a6\u06a8\3\2\2\2")
        buf.write("\u06a7\u06a2\3\2\2\2\u06a7\u06a3\3\2\2\2\u06a8\u06a9\3")
        buf.write("\2\2\2\u06a9\u06aa\5\u0098M\2\u06aa\u0151\3\2\2\2\u06ab")
        buf.write("\u06ae\5\u0154\u00ab\2\u06ac\u06ae\5\u0156\u00ac\2\u06ad")
        buf.write("\u06ab\3\2\2\2\u06ad\u06ac\3\2\2\2\u06ae\u0153\3\2\2\2")
        buf.write("\u06af\u06b0\5\u01c6\u00e4\2\u06b0\u06b1\7\61\2\2\u06b1")
        buf.write("\u06b2\7\7\2\2\u06b2\u0155\3\2\2\2\u06b3\u06b4\5@!\2\u06b4")
        buf.write("\u06b5\7e\2\2\u06b5\u06b7\7\27\2\2\u06b6\u06b8\5<\37\2")
        buf.write("\u06b7\u06b6\3\2\2\2\u06b7\u06b8\3\2\2\2\u06b8\u06b9\3")
        buf.write("\2\2\2\u06b9\u06bc\7\30\2\2\u06ba\u06bb\7<\2\2\u06bb\u06bd")
        buf.write("\5\u0178\u00bd\2\u06bc\u06ba\3\2\2\2\u06bc\u06bd\3\2\2")
        buf.write("\2\u06bd\u06be\3\2\2\2\u06be\u06bf\5\u0158\u00ad\2\u06bf")
        buf.write("\u0157\3\2\2\2\u06c0\u06c1\5\u0098M\2\u06c1\u0159\3\2")
        buf.write("\2\2\u06c2\u06c3\7x\2\2\u06c3\u06cc\7\33\2\2\u06c4\u06c9")
        buf.write("\5\u015c\u00af\2\u06c5\u06c6\7 \2\2\u06c6\u06c8\5\u015c")
        buf.write("\u00af\2\u06c7\u06c5\3\2\2\2\u06c8\u06cb\3\2\2\2\u06c9")
        buf.write("\u06c7\3\2\2\2\u06c9\u06ca\3\2\2\2\u06ca\u06cd\3\2\2\2")
        buf.write("\u06cb\u06c9\3\2\2\2\u06cc\u06c4\3\2\2\2\u06cc\u06cd\3")
        buf.write("\2\2\2\u06cd\u06ce\3\2\2\2\u06ce\u06cf\7\34\2\2\u06cf")
        buf.write("\u015b\3\2\2\2\u06d0\u06d1\5N(\2\u06d1\u06d2\t\30\2\2")
        buf.write("\u06d2\u06d3\5N(\2\u06d3\u015d\3\2\2\2\u06d4\u06d7\5\u0160")
        buf.write("\u00b1\2\u06d5\u06d7\5\u0162\u00b2\2\u06d6\u06d4\3\2\2")
        buf.write("\2\u06d6\u06d5\3\2\2\2\u06d7\u015f\3\2\2\2\u06d8\u06e1")
        buf.write("\7\31\2\2\u06d9\u06de\5N(\2\u06da\u06db\7 \2\2\u06db\u06dd")
        buf.write("\5N(\2\u06dc\u06da\3\2\2\2\u06dd\u06e0\3\2\2\2\u06de\u06dc")
        buf.write("\3\2\2\2\u06de\u06df\3\2\2\2\u06df\u06e2\3\2\2\2\u06e0")
        buf.write("\u06de\3\2\2\2\u06e1\u06d9\3\2\2\2\u06e1\u06e2\3\2\2\2")
        buf.write("\u06e2\u06e3\3\2\2\2\u06e3\u06e4\7\32\2\2\u06e4\u0161")
        buf.write("\3\2\2\2\u06e5\u06e6\7;\2\2\u06e6\u06e7\5\u0098M\2\u06e7")
        buf.write("\u0163\3\2\2\2\u06e8\u06e9\7\u00c4\2\2\u06e9\u06ea\5\u0166")
        buf.write("\u00b4\2\u06ea\u06eb\7\u00c9\2\2\u06eb\u0165\3\2\2\2\u06ec")
        buf.write("\u06f2\5\u016e\u00b8\2\u06ed\u06ee\5\u0170\u00b9\2\u06ee")
        buf.write("\u06ef\5\u016e\u00b8\2\u06ef\u06f1\3\2\2\2\u06f0\u06ed")
        buf.write("\3\2\2\2\u06f1\u06f4\3\2\2\2\u06f2\u06f0\3\2\2\2\u06f2")
        buf.write("\u06f3\3\2\2\2\u06f3\u0167\3\2\2\2\u06f4\u06f2\3\2\2\2")
        buf.write("\u06f5\u06f6\t\31\2\2\u06f6\u0169\3\2\2\2\u06f7\u06f8")
        buf.write("\t\32\2\2\u06f8\u016b\3\2\2\2\u06f9\u06fa\t\33\2\2\u06fa")
        buf.write("\u016d\3\2\2\2\u06fb\u0706\7\u00c7\2\2\u06fc\u06fd\5\u0168")
        buf.write("\u00b5\2\u06fd\u06fe\5\u016a\u00b6\2\u06fe\u0706\3\2\2")
        buf.write("\2\u06ff\u0700\5\u016c\u00b7\2\u0700\u0701\5\u0168\u00b5")
        buf.write("\2\u0701\u0702\5\u0168\u00b5\2\u0702\u0706\3\2\2\2\u0703")
        buf.write("\u0706\5\u0168\u00b5\2\u0704\u0706\7\33\2\2\u0705\u06fb")
        buf.write("\3\2\2\2\u0705\u06fc\3\2\2\2\u0705\u06ff\3\2\2\2\u0705")
        buf.write("\u0703\3\2\2\2\u0705\u0704\3\2\2\2\u0706\u0709\3\2\2\2")
        buf.write("\u0707\u0705\3\2\2\2\u0707\u0708\3\2\2\2\u0708\u016f\3")
        buf.write("\2\2\2\u0709\u0707\3\2\2\2\u070a\u070b\7\u00c8\2\2\u070b")
        buf.write("\u070c\5L\'\2\u070c\u070d\7\u00c5\2\2\u070d\u0171\3\2")
        buf.write("\2\2\u070e\u070f\7,\2\2\u070f\u0710\5\u00fa~\2\u0710\u0173")
        buf.write("\3\2\2\2\u0711\u0713\5\u01a0\u00d1\2\u0712\u0714\7,\2")
        buf.write("\2\u0713\u0712\3\2\2\2\u0713\u0714\3\2\2\2\u0714\u0175")
        buf.write("\3\2\2\2\u0715\u0716\7<\2\2\u0716\u0717\5\u0178\u00bd")
        buf.write("\2\u0717\u0177\3\2\2\2\u0718\u0719\7[\2\2\u0719\u071a")
        buf.write("\7\27\2\2\u071a\u0720\7\30\2\2\u071b\u071d\5\u017a\u00be")
        buf.write("\2\u071c\u071e\t\34\2\2\u071d\u071c\3\2\2\2\u071d\u071e")
        buf.write("\3\2\2\2\u071e\u0720\3\2\2\2\u071f\u0718\3\2\2\2\u071f")
        buf.write("\u071b\3\2\2\2\u0720\u0179\3\2\2\2\u0721\u072b\5\u017e")
        buf.write("\u00c0\2\u0722\u0723\7r\2\2\u0723\u0724\7\27\2\2\u0724")
        buf.write("\u072b\7\30\2\2\u0725\u072b\5\u01a4\u00d3\2\u0726\u072b")
        buf.write("\5\u01aa\u00d6\2\u0727\u072b\5\u01b0\u00d9\2\u0728\u072b")
        buf.write("\5\u017c\u00bf\2\u0729\u072b\5\u01b6\u00dc\2\u072a\u0721")
        buf.write("\3\2\2\2\u072a\u0722\3\2\2\2\u072a\u0725\3\2\2\2\u072a")
        buf.write("\u0726\3\2\2\2\u072a\u0727\3\2\2\2\u072a\u0728\3\2\2\2")
        buf.write("\u072a\u0729\3\2\2\2\u072b\u017b\3\2\2\2\u072c\u072d\5")
        buf.write("\u01c6\u00e4\2\u072d\u017d\3\2\2\2\u072e\u073b\5\u0184")
        buf.write("\u00c3\2\u072f\u073b\5\u0194\u00cb\2\u0730\u073b\5\u018e")
        buf.write("\u00c8\2\u0731\u073b\5\u0198\u00cd\2\u0732\u073b\5\u0192")
        buf.write("\u00ca\2\u0733\u073b\5\u018c\u00c7\2\u0734\u073b\5\u0188")
        buf.write("\u00c5\2\u0735\u073b\5\u0186\u00c4\2\u0736\u073b\5\u018a")
        buf.write("\u00c6\2\u0737\u073b\5\u01ba\u00de\2\u0738\u073b\5\u0182")
        buf.write("\u00c2\2\u0739\u073b\5\u0180\u00c1\2\u073a\u072e\3\2\2")
        buf.write("\2\u073a\u072f\3\2\2\2\u073a\u0730\3\2\2\2\u073a\u0731")
        buf.write("\3\2\2\2\u073a\u0732\3\2\2\2\u073a\u0733\3\2\2\2\u073a")
        buf.write("\u0734\3\2\2\2\u073a\u0735\3\2\2\2\u073a\u0736\3\2\2\2")
        buf.write("\u073a\u0737\3\2\2\2\u073a\u0738\3\2\2\2\u073a\u0739\3")
        buf.write("\2\2\2\u073b\u017f\3\2\2\2\u073c\u073d\7\u0081\2\2\u073d")
        buf.write("\u073f\7\27\2\2\u073e\u0740\7\35\2\2\u073f\u073e\3\2\2")
        buf.write("\2\u073f\u0740\3\2\2\2\u0740\u0741\3\2\2\2\u0741\u0742")
        buf.write("\7\30\2\2\u0742\u0181\3\2\2\2\u0743\u0744\7B\2\2\u0744")
        buf.write("\u0745\7\27\2\2\u0745\u0746\7\30\2\2\u0746\u0183\3\2\2")
        buf.write("\2\u0747\u0748\7W\2\2\u0748\u074b\7\27\2\2\u0749\u074c")
        buf.write("\5\u0194\u00cb\2\u074a\u074c\5\u0198\u00cd\2\u074b\u0749")
        buf.write("\3\2\2\2\u074b\u074a\3\2\2\2\u074b\u074c\3\2\2\2\u074c")
        buf.write("\u074d\3\2\2\2\u074d\u074e\7\30\2\2\u074e\u0185\3\2\2")
        buf.write("\2\u074f\u0750\7\u009c\2\2\u0750\u0751\7\27\2\2\u0751")
        buf.write("\u0752\7\30\2\2\u0752\u0187\3\2\2\2\u0753\u0754\7J\2\2")
        buf.write("\u0754\u0755\7\27\2\2\u0755\u0756\7\30\2\2\u0756\u0189")
        buf.write("\3\2\2\2\u0757\u0758\7~\2\2\u0758\u0759\7\27\2\2\u0759")
        buf.write("\u075a\7\30\2\2\u075a\u018b\3\2\2\2\u075b\u075c\7\u008e")
        buf.write("\2\2\u075c\u075f\7\27\2\2\u075d\u0760\5\u01ca\u00e6\2")
        buf.write("\u075e\u0760\5\u01da\u00ee\2\u075f\u075d\3\2\2\2\u075f")
        buf.write("\u075e\3\2\2\2\u075f\u0760\3\2\2\2\u0760\u0761\3\2\2\2")
        buf.write("\u0761\u0762\7\30\2\2\u0762\u018d\3\2\2\2\u0763\u0764")
        buf.write("\7?\2\2\u0764\u076a\7\27\2\2\u0765\u0768\5\u0190\u00c9")
        buf.write("\2\u0766\u0767\7 \2\2\u0767\u0769\5\u01a2\u00d2\2\u0768")
        buf.write("\u0766\3\2\2\2\u0768\u0769\3\2\2\2\u0769\u076b\3\2\2\2")
        buf.write("\u076a\u0765\3\2\2\2\u076a\u076b\3\2\2\2\u076b\u076c\3")
        buf.write("\2\2\2\u076c\u076d\7\30\2\2\u076d\u018f\3\2\2\2\u076e")
        buf.write("\u0771\5\u019c\u00cf\2\u076f\u0771\7\35\2\2\u0770\u076e")
        buf.write("\3\2\2\2\u0770\u076f\3\2\2\2\u0771\u0191\3\2\2\2\u0772")
        buf.write("\u0773\7\u0092\2\2\u0773\u0774\7\27\2\2\u0774\u0775\5")
        buf.write("\u01b8\u00dd\2\u0775\u0776\7\30\2\2\u0776\u0193\3\2\2")
        buf.write("\2\u0777\u0778\7X\2\2\u0778\u0781\7\27\2\2\u0779\u077f")
        buf.write("\5\u0196\u00cc\2\u077a\u077b\7 \2\2\u077b\u077d\5\u01a2")
        buf.write("\u00d2\2\u077c\u077e\7,\2\2\u077d\u077c\3\2\2\2\u077d")
        buf.write("\u077e\3\2\2\2\u077e\u0780\3\2\2\2\u077f\u077a\3\2\2\2")
        buf.write("\u077f\u0780\3\2\2\2\u0780\u0782\3\2\2\2\u0781\u0779\3")
        buf.write("\2\2\2\u0781\u0782\3\2\2\2\u0782\u0783\3\2\2\2\u0783\u0784")
        buf.write("\7\30\2\2\u0784\u0195\3\2\2\2\u0785\u0788\5\u019e\u00d0")
        buf.write("\2\u0786\u0788\7\35\2\2\u0787\u0785\3\2\2\2\u0787\u0786")
        buf.write("\3\2\2\2\u0788\u0197\3\2\2\2\u0789\u078a\7\u0093\2\2\u078a")
        buf.write("\u078b\7\27\2\2\u078b\u078c\5\u019a\u00ce\2\u078c\u078d")
        buf.write("\7\30\2\2\u078d\u0199\3\2\2\2\u078e\u078f\5\u019e\u00d0")
        buf.write("\2\u078f\u019b\3\2\2\2\u0790\u0791\5\u01c6\u00e4\2\u0791")
        buf.write("\u019d\3\2\2\2\u0792\u0793\5\u01c6\u00e4\2\u0793\u019f")
        buf.write("\3\2\2\2\u0794\u0795\5\u01a2\u00d2\2\u0795\u01a1\3\2\2")
        buf.write("\2\u0796\u0797\5\u01c6\u00e4\2\u0797\u01a3\3\2\2\2\u0798")
        buf.write("\u079a\5B\"\2\u0799\u0798\3\2\2\2\u079a\u079d\3\2\2\2")
        buf.write("\u079b\u0799\3\2\2\2\u079b\u079c\3\2\2\2\u079c\u07a0\3")
        buf.write("\2\2\2\u079d\u079b\3\2\2\2\u079e\u07a1\5\u01a6\u00d4\2")
        buf.write("\u079f\u07a1\5\u01a8\u00d5\2\u07a0\u079e\3\2\2\2\u07a0")
        buf.write("\u079f\3\2\2\2\u07a1\u01a5\3\2\2\2\u07a2\u07a3\7e\2\2")
        buf.write("\u07a3\u07a4\7\27\2\2\u07a4\u07a5\7\35\2\2\u07a5\u07a6")
        buf.write("\7\30\2\2\u07a6\u01a7\3\2\2\2\u07a7\u07a8\7e\2\2\u07a8")
        buf.write("\u07b1\7\27\2\2\u07a9\u07ae\5\u0178\u00bd\2\u07aa\u07ab")
        buf.write("\7 \2\2\u07ab\u07ad\5\u0178\u00bd\2\u07ac\u07aa\3\2\2")
        buf.write("\2\u07ad\u07b0\3\2\2\2\u07ae\u07ac\3\2\2\2\u07ae\u07af")
        buf.write("\3\2\2\2\u07af\u07b2\3\2\2\2\u07b0\u07ae\3\2\2\2\u07b1")
        buf.write("\u07a9\3\2\2\2\u07b1\u07b2\3\2\2\2\u07b2\u07b3\3\2\2\2")
        buf.write("\u07b3\u07b4\7\30\2\2\u07b4\u07b5\7<\2\2\u07b5\u07b6\5")
        buf.write("\u0178\u00bd\2\u07b6\u01a9\3\2\2\2\u07b7\u07ba\5\u01ac")
        buf.write("\u00d7\2\u07b8\u07ba\5\u01ae\u00d8\2\u07b9\u07b7\3\2\2")
        buf.write("\2\u07b9\u07b8\3\2\2\2\u07ba\u01ab\3\2\2\2\u07bb\u07bc")
        buf.write("\7x\2\2\u07bc\u07bd\7\27\2\2\u07bd\u07be\7\35\2\2\u07be")
        buf.write("\u07bf\7\30\2\2\u07bf\u01ad\3\2\2\2\u07c0\u07c1\7x\2\2")
        buf.write("\u07c1\u07c2\7\27\2\2\u07c2\u07c3\5\u01c6\u00e4\2\u07c3")
        buf.write("\u07c4\7 \2\2\u07c4\u07c5\5\u0178\u00bd\2\u07c5\u07c6")
        buf.write("\7\30\2\2\u07c6\u01af\3\2\2\2\u07c7\u07ca\5\u01b2\u00da")
        buf.write("\2\u07c8\u07ca\5\u01b4\u00db\2\u07c9\u07c7\3\2\2\2\u07c9")
        buf.write("\u07c8\3\2\2\2\u07ca\u01b1\3\2\2\2\u07cb\u07cc\7;\2\2")
        buf.write("\u07cc\u07cd\7\27\2\2\u07cd\u07ce\7\35\2\2\u07ce\u07cf")
        buf.write("\7\30\2\2\u07cf\u01b3\3\2\2\2\u07d0\u07d1\7;\2\2\u07d1")
        buf.write("\u07d2\7\27\2\2\u07d2\u07d3\5\u0178\u00bd\2\u07d3\u07d4")
        buf.write("\7\30\2\2\u07d4\u01b5\3\2\2\2\u07d5\u07d6\7\27\2\2\u07d6")
        buf.write("\u07d7\5\u017a\u00be\2\u07d7\u07d8\7\30\2\2\u07d8\u01b7")
        buf.write("\3\2\2\2\u07d9\u07da\5\u019c\u00cf\2\u07da\u01b9\3\2\2")
        buf.write("\2\u07db\u07e1\5\u01bc\u00df\2\u07dc\u07e1\5\u01be\u00e0")
        buf.write("\2\u07dd\u07e1\5\u01c0\u00e1\2\u07de\u07e1\5\u01c2\u00e2")
        buf.write("\2\u07df\u07e1\5\u01c4\u00e3\2\u07e0\u07db\3\2\2\2\u07e0")
        buf.write("\u07dc\3\2\2\2\u07e0\u07dd\3\2\2\2\u07e0\u07de\3\2\2\2")
        buf.write("\u07e0\u07df\3\2\2\2\u07e1\u01bb\3\2\2\2\u07e2\u07e3\7")
        buf.write("\u00ae\2\2\u07e3\u07e5\7\27\2\2\u07e4\u07e6\5\u01da\u00ee")
        buf.write("\2\u07e5\u07e4\3\2\2\2\u07e5\u07e6\3\2\2\2\u07e6\u07e7")
        buf.write("\3\2\2\2\u07e7\u07e8\7\30\2\2\u07e8\u01bd\3\2\2\2\u07e9")
        buf.write("\u07ea\7\u00b2\2\2\u07ea\u07ec\7\27\2\2\u07eb\u07ed\5")
        buf.write("\u01da\u00ee\2\u07ec\u07eb\3\2\2\2\u07ec\u07ed\3\2\2\2")
        buf.write("\u07ed\u07ee\3\2\2\2\u07ee\u07ef\7\30\2\2\u07ef\u01bf")
        buf.write("\3\2\2\2\u07f0\u07f1\7\u00b1\2\2\u07f1\u07f3\7\27\2\2")
        buf.write("\u07f2\u07f4\5\u01da\u00ee\2\u07f3\u07f2\3\2\2\2\u07f3")
        buf.write("\u07f4\3\2\2\2\u07f4\u07f5\3\2\2\2\u07f5\u07f6\7\30\2")
        buf.write("\2\u07f6\u01c1\3\2\2\2\u07f7\u07f8\7\u00af\2\2\u07f8\u07fa")
        buf.write("\7\27\2\2\u07f9\u07fb\5\u01da\u00ee\2\u07fa\u07f9\3\2")
        buf.write("\2\2\u07fa\u07fb\3\2\2\2\u07fb\u07fc\3\2\2\2\u07fc\u07fd")
        buf.write("\7\30\2\2\u07fd\u01c3\3\2\2\2\u07fe\u07ff\7\u00b0\2\2")
        buf.write("\u07ff\u0801\7\27\2\2\u0800\u0802\5\u01da\u00ee\2\u0801")
        buf.write("\u0800\3\2\2\2\u0801\u0802\3\2\2\2\u0802\u0803\3\2\2\2")
        buf.write("\u0803\u0804\7\30\2\2\u0804\u01c5\3\2\2\2\u0805\u0808")
        buf.write("\5\u01c8\u00e5\2\u0806\u0808\7\u00ba\2\2\u0807\u0805\3")
        buf.write("\2\2\2\u0807\u0806\3\2\2\2\u0808\u01c7\3\2\2\2\u0809\u080c")
        buf.write("\7\u00bb\2\2\u080a\u080c\5\u01ca\u00e6\2\u080b\u0809\3")
        buf.write("\2\2\2\u080b\u080a\3\2\2\2\u080c\u01c9\3\2\2\2\u080d\u0810")
        buf.write("\7\u00be\2\2\u080e\u0810\5\u01ce\u00e8\2\u080f\u080d\3")
        buf.write("\2\2\2\u080f\u080e\3\2\2\2\u0810\u01cb\3\2\2\2\u0811\u0816")
        buf.write("\7\u00bb\2\2\u0812\u0816\7\u00be\2\2\u0813\u0816\7\u00ba")
        buf.write("\2\2\u0814\u0816\5\u01d2\u00ea\2\u0815\u0811\3\2\2\2\u0815")
        buf.write("\u0812\3\2\2\2\u0815\u0813\3\2\2\2\u0815\u0814\3\2\2\2")
        buf.write("\u0816\u01cd\3\2\2\2\u0817\u081a\5\u01d2\u00ea\2\u0818")
        buf.write("\u081a\5\u01d0\u00e9\2\u0819\u0817\3\2\2\2\u0819\u0818")
        buf.write("\3\2\2\2\u081a\u01cf\3\2\2\2\u081b\u081c\t\35\2\2\u081c")
        buf.write("\u01d1\3\2\2\2\u081d\u081e\t\36\2\2\u081e\u01d3\3\2\2")
        buf.write("\2\u081f\u0820\5\u01da\u00ee\2\u0820\u01d5\3\2\2\2\u0821")
        buf.write("\u0828\7\r\2\2\u0822\u0827\7\13\2\2\u0823\u0827\7\f\2")
        buf.write("\2\u0824\u0827\7\3\2\2\u0825\u0827\5\u01dc\u00ef\2\u0826")
        buf.write("\u0822\3\2\2\2\u0826\u0823\3\2\2\2\u0826\u0824\3\2\2\2")
        buf.write("\u0826\u0825\3\2\2\2\u0827\u082a\3\2\2\2\u0828\u0826\3")
        buf.write("\2\2\2\u0828\u0829\3\2\2\2\u0829\u082b\3\2\2\2\u082a\u0828")
        buf.write("\3\2\2\2\u082b\u082c\7\r\2\2\u082c\u01d7\3\2\2\2\u082d")
        buf.write("\u0834\7\16\2\2\u082e\u0833\7\13\2\2\u082f\u0833\7\f\2")
        buf.write("\2\u0830\u0833\7\4\2\2\u0831\u0833\5\u01de\u00f0\2\u0832")
        buf.write("\u082e\3\2\2\2\u0832\u082f\3\2\2\2\u0832\u0830\3\2\2\2")
        buf.write("\u0832\u0831\3\2\2\2\u0833\u0836\3\2\2\2\u0834\u0832\3")
        buf.write("\2\2\2\u0834\u0835\3\2\2\2\u0835\u0837\3\2\2\2\u0836\u0834")
        buf.write("\3\2\2\2\u0837\u0838\7\16\2\2\u0838\u01d9\3\2\2\2\u0839")
        buf.write("\u083c\5\u01d6\u00ec\2\u083a\u083c\5\u01d8\u00ed\2\u083b")
        buf.write("\u0839\3\2\2\2\u083b\u083a\3\2\2\2\u083c\u01db\3\2\2\2")
        buf.write("\u083d\u083f\7\u00c6\2\2\u083e\u083d\3\2\2\2\u083f\u0840")
        buf.write("\3\2\2\2\u0840\u083e\3\2\2\2\u0840\u0841\3\2\2\2\u0841")
        buf.write("\u084f\3\2\2\2\u0842\u0844\7\33\2\2\u0843\u0845\5L\'\2")
        buf.write("\u0844\u0843\3\2\2\2\u0844\u0845\3\2\2\2\u0845\u0847\3")
        buf.write("\2\2\2\u0846\u0848\7\34\2\2\u0847\u0846\3\2\2\2\u0847")
        buf.write("\u0848\3\2\2\2\u0848\u084f\3\2\2\2\u0849\u084f\7\34\2")
        buf.write("\2\u084a\u084f\7\5\2\2\u084b\u084f\7\6\2\2\u084c\u084f")
        buf.write("\5\u01e0\u00f1\2\u084d\u084f\5\u01d8\u00ed\2\u084e\u083e")
        buf.write("\3\2\2\2\u084e\u0842\3\2\2\2\u084e\u0849\3\2\2\2\u084e")
        buf.write("\u084a\3\2\2\2\u084e\u084b\3\2\2\2\u084e\u084c\3\2\2\2")
        buf.write("\u084e\u084d\3\2\2\2\u084f\u01dd\3\2\2\2\u0850\u0852\7")
        buf.write("\u00c6\2\2\u0851\u0850\3\2\2\2\u0852\u0853\3\2\2\2\u0853")
        buf.write("\u0851\3\2\2\2\u0853\u0854\3\2\2\2\u0854\u0862\3\2\2\2")
        buf.write("\u0855\u0857\7\33\2\2\u0856\u0858\5L\'\2\u0857\u0856\3")
        buf.write("\2\2\2\u0857\u0858\3\2\2\2\u0858\u085a\3\2\2\2\u0859\u085b")
        buf.write("\7\34\2\2\u085a\u0859\3\2\2\2\u085a\u085b\3\2\2\2\u085b")
        buf.write("\u0862\3\2\2\2\u085c\u0862\7\34\2\2\u085d\u0862\7\5\2")
        buf.write("\2\u085e\u0862\7\6\2\2\u085f\u0862\5\u01e0\u00f1\2\u0860")
        buf.write("\u0862\5\u01d6\u00ec\2\u0861\u0851\3\2\2\2\u0861\u0855")
        buf.write("\3\2\2\2\u0861\u085c\3\2\2\2\u0861\u085d\3\2\2\2\u0861")
        buf.write("\u085e\3\2\2\2\u0861\u085f\3\2\2\2\u0861\u0860\3\2\2\2")
        buf.write("\u0862\u01df\3\2\2\2\u0863\u0866\5\u01ce\u00e8\2\u0864")
        buf.write("\u0866\t\37\2\2\u0865\u0863\3\2\2\2\u0865\u0864\3\2\2")
        buf.write("\2\u0866\u0867\3\2\2\2\u0867\u0865\3\2\2\2\u0867\u0868")
        buf.write("\3\2\2\2\u0868\u01e1\3\2\2\2\u00d2\u01e3\u01e6\u01e9\u01ef")
        buf.write("\u01f4\u01f7\u0200\u0218\u021e\u0222\u0228\u022e\u023f")
        buf.write("\u026b\u0272\u0278\u0281\u0284\u028d\u0295\u029e\u02a1")
        buf.write("\u02ac\u02b2\u02b9\u02c4\u02c6\u02d1\u02d8\u02da\u02df")
        buf.write("\u02e5\u02e9\u02ed\u02f4\u02fa\u02ff\u0308\u030f\u0321")
        buf.write("\u032c\u0332\u033a\u0341\u0349\u034f\u0352\u0355\u0367")
        buf.write("\u036d\u0375\u037c\u0382\u0389\u0396\u039f\u03a2\u03a7")
        buf.write("\u03ac\u03be\u03c4\u03c8\u03cc\u03cf\u03d8\u03dd\u03e1")
        buf.write("\u03e5\u03f0\u03f9\u0405\u040f\u041d\u0422\u042c\u0437")
        buf.write("\u0447\u0455\u045b\u0464\u046d\u048b\u0493\u049a\u049e")
        buf.write("\u04a5\u04ab\u04b2\u04ba\u04c2\u04ca\u04d1\u04d7\u04dd")
        buf.write("\u04e3\u04ec\u04f2\u04fa\u0504\u050d\u0513\u051c\u0527")
        buf.write("\u052c\u0531\u0538\u053d\u0541\u0549\u0550\u0558\u0562")
        buf.write("\u0566\u056b\u0571\u0573\u057c\u057f\u0586\u0594\u0599")
        buf.write("\u05a8\u05ac\u05b7\u05c8\u05cc\u05d1\u05da\u05ee\u05f6")
        buf.write("\u05f8\u0602\u0604\u060b\u0610\u0617\u061a\u061f\u0626")
        buf.write("\u0629\u0631\u063c\u0646\u064e\u065f\u0662\u067e\u068a")
        buf.write("\u0691\u06a7\u06ad\u06b7\u06bc\u06c9\u06cc\u06d6\u06de")
        buf.write("\u06e1\u06f2\u0705\u0707\u0713\u071d\u071f\u072a\u073a")
        buf.write("\u073f\u074b\u075f\u0768\u076a\u0770\u077d\u077f\u0781")
        buf.write("\u0787\u079b\u07a0\u07ae\u07b1\u07b9\u07c9\u07e0\u07e5")
        buf.write("\u07ec\u07f3\u07fa\u0801\u0807\u080b\u080f\u0815\u0819")
        buf.write("\u0826\u0828\u0832\u0834\u083b\u0840\u0844\u0847\u084e")
        buf.write("\u0853\u0857\u085a\u0861\u0865\u0867")
        return buf.getvalue()


class XQueryParser ( Parser ):

    grammarFileName = "XQueryParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "EscapeQuot", "EscapeApos", "DOUBLE_LBRACE", 
                      "DOUBLE_RBRACE", "IntegerLiteral", "DecimalLiteral", 
                      "DoubleLiteral", "DFPropertyName", "PredefinedEntityRef", 
                      "CharRef", "Quot", "Apos", "COMMENT", "XMLDECL", "PI", 
                      "CDATA", "PRAGMA", "WS", "EQUAL", "NOT_EQUAL", "LPAREN", 
                      "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", 
                      "STAR", "PLUS", "MINUS", "COMMA", "DOT", "DDOT", "COLON", 
                      "COLON_EQ", "SEMICOLON", "SLASH", "DSLASH", "BACKSLASH", 
                      "VBAR", "LANGLE", "RANGLE", "QUESTION", "AT", "DOLLAR", 
                      "MOD", "BANG", "HASH", "CARAT", "ARROW", "GRAVE", 
                      "CONCATENATION", "TILDE", "KW_ALLOWING", "KW_ANCESTOR", 
                      "KW_ANCESTOR_OR_SELF", "KW_AND", "KW_ARRAY", "KW_AS", 
                      "KW_ASCENDING", "KW_AT", "KW_ATTRIBUTE", "KW_BASE_URI", 
                      "KW_BOUNDARY_SPACE", "KW_BINARY", "KW_BY", "KW_CASE", 
                      "KW_CAST", "KW_CASTABLE", "KW_CATCH", "KW_CHILD", 
                      "KW_COLLATION", "KW_COMMENT", "KW_CONSTRUCTION", "KW_CONTEXT", 
                      "KW_COPY_NS", "KW_COUNT", "KW_DECLARE", "KW_DEFAULT", 
                      "KW_DESCENDANT", "KW_DESCENDANT_OR_SELF", "KW_DESCENDING", 
                      "KW_DECIMAL_FORMAT", "KW_DIV", "KW_DOCUMENT", "KW_DOCUMENT_NODE", 
                      "KW_ELEMENT", "KW_ELSE", "KW_EMPTY", "KW_EMPTY_SEQUENCE", 
                      "KW_ENCODING", "KW_END", "KW_EQ", "KW_EVERY", "KW_EXCEPT", 
                      "KW_EXTERNAL", "KW_FOLLOWING", "KW_FOLLOWING_SIBLING", 
                      "KW_FOR", "KW_FUNCTION", "KW_GE", "KW_GREATEST", "KW_GROUP", 
                      "KW_GT", "KW_IDIV", "KW_IF", "KW_IMPORT", "KW_IN", 
                      "KW_INHERIT", "KW_INSTANCE", "KW_INTERSECT", "KW_IS", 
                      "KW_ITEM", "KW_LAX", "KW_LE", "KW_LEAST", "KW_LET", 
                      "KW_LT", "KW_MAP", "KW_MOD", "KW_MODULE", "KW_NAMESPACE", 
                      "KW_NE", "KW_NEXT", "KW_NAMESPACE_NODE", "KW_NO_INHERIT", 
                      "KW_NO_PRESERVE", "KW_NODE", "KW_OF", "KW_ONLY", "KW_OPTION", 
                      "KW_OR", "KW_ORDER", "KW_ORDERED", "KW_ORDERING", 
                      "KW_PARENT", "KW_PRECEDING", "KW_PRECEDING_SIBLING", 
                      "KW_PRESERVE", "KW_PREVIOUS", "KW_PI", "KW_RETURN", 
                      "KW_SATISFIES", "KW_SCHEMA", "KW_SCHEMA_ATTR", "KW_SCHEMA_ELEM", 
                      "KW_SELF", "KW_SLIDING", "KW_SOME", "KW_STABLE", "KW_START", 
                      "KW_STRICT", "KW_STRIP", "KW_SWITCH", "KW_TEXT", "KW_THEN", 
                      "KW_TO", "KW_TREAT", "KW_TRY", "KW_TUMBLING", "KW_TYPE", 
                      "KW_TYPESWITCH", "KW_UNION", "KW_UNORDERED", "KW_UPDATE", 
                      "KW_VALIDATE", "KW_VARIABLE", "KW_VERSION", "KW_WHEN", 
                      "KW_WHERE", "KW_WINDOW", "KW_XQUERY", "KW_ARRAY_NODE", 
                      "KW_BOOLEAN_NODE", "KW_NULL_NODE", "KW_NUMBER_NODE", 
                      "KW_OBJECT_NODE", "KW_REPLACE", "KW_WITH", "KW_VALUE", 
                      "KW_INSERT", "KW_INTO", "KW_DELETE", "KW_RENAME", 
                      "URIQualifiedName", "FullQName", "NCNameWithLocalWildcard", 
                      "NCNameWithPrefixWildcard", "NCName", "XQDOC_COMMENT_START", 
                      "XQDOC_COMMENT_END", "XQDocComment", "XQComment", 
                      "CHAR", "ENTER_STRING", "EXIT_INTERPOLATION", "ContentChar", 
                      "BASIC_CHAR", "ENTER_INTERPOLATION", "EXIT_STRING", 
                      "EscapeQuot_QuotString", "DOUBLE_LBRACE_QuotString", 
                      "DOUBLE_RBRACE_QuotString", "EscapeApos_AposString" ]

    RULE_module = 0
    RULE_xqDocComment = 1
    RULE_versionDecl = 2
    RULE_mainModule = 3
    RULE_queryBody = 4
    RULE_libraryModule = 5
    RULE_moduleDecl = 6
    RULE_prolog = 7
    RULE_defaultNamespaceDecl = 8
    RULE_setter = 9
    RULE_boundarySpaceDecl = 10
    RULE_defaultCollationDecl = 11
    RULE_baseURIDecl = 12
    RULE_constructionDecl = 13
    RULE_orderingModeDecl = 14
    RULE_emptyOrderDecl = 15
    RULE_copyNamespacesDecl = 16
    RULE_preserveMode = 17
    RULE_inheritMode = 18
    RULE_decimalFormatDecl = 19
    RULE_schemaImport = 20
    RULE_schemaPrefix = 21
    RULE_moduleImport = 22
    RULE_namespaceDecl = 23
    RULE_varDecl = 24
    RULE_varValue = 25
    RULE_varDefaultValue = 26
    RULE_contextItemDecl = 27
    RULE_functionDecl = 28
    RULE_functionParams = 29
    RULE_functionParam = 30
    RULE_annotations = 31
    RULE_annotation = 32
    RULE_annotList = 33
    RULE_annotationParam = 34
    RULE_functionReturn = 35
    RULE_optionDecl = 36
    RULE_expr = 37
    RULE_exprSingle = 38
    RULE_flworExpr = 39
    RULE_initialClause = 40
    RULE_intermediateClause = 41
    RULE_forClause = 42
    RULE_forBinding = 43
    RULE_allowingEmpty = 44
    RULE_positionalVar = 45
    RULE_letClause = 46
    RULE_letBinding = 47
    RULE_windowClause = 48
    RULE_tumblingWindowClause = 49
    RULE_slidingWindowClause = 50
    RULE_windowStartCondition = 51
    RULE_windowEndCondition = 52
    RULE_windowVars = 53
    RULE_countClause = 54
    RULE_whereClause = 55
    RULE_groupByClause = 56
    RULE_groupingSpecList = 57
    RULE_groupingSpec = 58
    RULE_orderByClause = 59
    RULE_orderSpec = 60
    RULE_returnClause = 61
    RULE_quantifiedExpr = 62
    RULE_quantifiedVar = 63
    RULE_switchExpr = 64
    RULE_switchCaseClause = 65
    RULE_switchCaseOperand = 66
    RULE_typeswitchExpr = 67
    RULE_caseClause = 68
    RULE_sequenceUnionType = 69
    RULE_ifExpr = 70
    RULE_tryCatchExpr = 71
    RULE_tryClause = 72
    RULE_enclosedTryTargetExpression = 73
    RULE_catchClause = 74
    RULE_enclosedExpression = 75
    RULE_catchErrorList = 76
    RULE_existUpdateExpr = 77
    RULE_existReplaceExpr = 78
    RULE_existValueExpr = 79
    RULE_existInsertExpr = 80
    RULE_existDeleteExpr = 81
    RULE_existRenameExpr = 82
    RULE_orExpr = 83
    RULE_andExpr = 84
    RULE_comparisonExpr = 85
    RULE_stringConcatExpr = 86
    RULE_rangeExpr = 87
    RULE_additiveExpr = 88
    RULE_multiplicativeExpr = 89
    RULE_unionExpr = 90
    RULE_intersectExceptExpr = 91
    RULE_instanceOfExpr = 92
    RULE_treatExpr = 93
    RULE_castableExpr = 94
    RULE_castExpr = 95
    RULE_arrowExpr = 96
    RULE_unaryExpression = 97
    RULE_valueExpr = 98
    RULE_generalComp = 99
    RULE_valueComp = 100
    RULE_nodeComp = 101
    RULE_validateExpr = 102
    RULE_validationMode = 103
    RULE_extensionExpr = 104
    RULE_simpleMapExpr = 105
    RULE_pathExpr = 106
    RULE_relativePathExpr = 107
    RULE_stepExpr = 108
    RULE_axisStep = 109
    RULE_forwardStep = 110
    RULE_forwardAxis = 111
    RULE_abbrevForwardStep = 112
    RULE_reverseStep = 113
    RULE_reverseAxis = 114
    RULE_abbrevReverseStep = 115
    RULE_nodeTest = 116
    RULE_nameTest = 117
    RULE_wildcard = 118
    RULE_postfixExpr = 119
    RULE_argumentList = 120
    RULE_predicateList = 121
    RULE_predicate = 122
    RULE_lookup = 123
    RULE_keySpecifier = 124
    RULE_arrowFunctionSpecifier = 125
    RULE_primaryExpr = 126
    RULE_literal = 127
    RULE_numericLiteral = 128
    RULE_varRef = 129
    RULE_varName = 130
    RULE_parenthesizedExpr = 131
    RULE_contextItemExpr = 132
    RULE_orderedExpr = 133
    RULE_unorderedExpr = 134
    RULE_functionCall = 135
    RULE_argument = 136
    RULE_nodeConstructor = 137
    RULE_directConstructor = 138
    RULE_dirElemConstructorOpenClose = 139
    RULE_dirElemConstructorSingleTag = 140
    RULE_dirAttributeList = 141
    RULE_dirAttributeValueApos = 142
    RULE_dirAttributeValueQuot = 143
    RULE_dirAttributeValue = 144
    RULE_dirAttributeContentQuot = 145
    RULE_dirAttributeContentApos = 146
    RULE_dirElemContent = 147
    RULE_commonContent = 148
    RULE_computedConstructor = 149
    RULE_compMLJSONConstructor = 150
    RULE_compMLJSONArrayConstructor = 151
    RULE_compMLJSONObjectConstructor = 152
    RULE_compMLJSONNumberConstructor = 153
    RULE_compMLJSONBooleanConstructor = 154
    RULE_compMLJSONNullConstructor = 155
    RULE_compBinaryConstructor = 156
    RULE_compDocConstructor = 157
    RULE_compElemConstructor = 158
    RULE_enclosedContentExpr = 159
    RULE_compAttrConstructor = 160
    RULE_compNamespaceConstructor = 161
    RULE_prefix = 162
    RULE_enclosedPrefixExpr = 163
    RULE_enclosedURIExpr = 164
    RULE_compTextConstructor = 165
    RULE_compCommentConstructor = 166
    RULE_compPIConstructor = 167
    RULE_functionItemExpr = 168
    RULE_namedFunctionRef = 169
    RULE_inlineFunctionRef = 170
    RULE_functionBody = 171
    RULE_mapConstructor = 172
    RULE_mapConstructorEntry = 173
    RULE_arrayConstructor = 174
    RULE_squareArrayConstructor = 175
    RULE_curlyArrayConstructor = 176
    RULE_stringConstructor = 177
    RULE_stringConstructorContent = 178
    RULE_charNoGrave = 179
    RULE_charNoLBrace = 180
    RULE_charNoRBrack = 181
    RULE_stringConstructorChars = 182
    RULE_stringConstructorInterpolation = 183
    RULE_unaryLookup = 184
    RULE_singleType = 185
    RULE_typeDeclaration = 186
    RULE_sequenceType = 187
    RULE_itemType = 188
    RULE_atomicOrUnionType = 189
    RULE_kindTest = 190
    RULE_anyKindTest = 191
    RULE_binaryNodeTest = 192
    RULE_documentTest = 193
    RULE_textTest = 194
    RULE_commentTest = 195
    RULE_namespaceNodeTest = 196
    RULE_piTest = 197
    RULE_attributeTest = 198
    RULE_attributeNameOrWildcard = 199
    RULE_schemaAttributeTest = 200
    RULE_elementTest = 201
    RULE_elementNameOrWildcard = 202
    RULE_schemaElementTest = 203
    RULE_elementDeclaration = 204
    RULE_attributeName = 205
    RULE_elementName = 206
    RULE_simpleTypeName = 207
    RULE_typeName = 208
    RULE_functionTest = 209
    RULE_anyFunctionTest = 210
    RULE_typedFunctionTest = 211
    RULE_mapTest = 212
    RULE_anyMapTest = 213
    RULE_typedMapTest = 214
    RULE_arrayTest = 215
    RULE_anyArrayTest = 216
    RULE_typedArrayTest = 217
    RULE_parenthesizedItemTest = 218
    RULE_attributeDeclaration = 219
    RULE_mlNodeTest = 220
    RULE_mlArrayNodeTest = 221
    RULE_mlObjectNodeTest = 222
    RULE_mlNumberNodeTest = 223
    RULE_mlBooleanNodeTest = 224
    RULE_mlNullNodeTest = 225
    RULE_eqName = 226
    RULE_qName = 227
    RULE_ncName = 228
    RULE_functionName = 229
    RULE_keyword = 230
    RULE_keywordNotOKForFunction = 231
    RULE_keywordOKForFunction = 232
    RULE_uriLiteral = 233
    RULE_stringLiteralQuot = 234
    RULE_stringLiteralApos = 235
    RULE_stringLiteral = 236
    RULE_stringContentQuot = 237
    RULE_stringContentApos = 238
    RULE_noQuotesNoBracesNoAmpNoLAng = 239

    ruleNames =  [ "module", "xqDocComment", "versionDecl", "mainModule", 
                   "queryBody", "libraryModule", "moduleDecl", "prolog", 
                   "defaultNamespaceDecl", "setter", "boundarySpaceDecl", 
                   "defaultCollationDecl", "baseURIDecl", "constructionDecl", 
                   "orderingModeDecl", "emptyOrderDecl", "copyNamespacesDecl", 
                   "preserveMode", "inheritMode", "decimalFormatDecl", "schemaImport", 
                   "schemaPrefix", "moduleImport", "namespaceDecl", "varDecl", 
                   "varValue", "varDefaultValue", "contextItemDecl", "functionDecl", 
                   "functionParams", "functionParam", "annotations", "annotation", 
                   "annotList", "annotationParam", "functionReturn", "optionDecl", 
                   "expr", "exprSingle", "flworExpr", "initialClause", "intermediateClause", 
                   "forClause", "forBinding", "allowingEmpty", "positionalVar", 
                   "letClause", "letBinding", "windowClause", "tumblingWindowClause", 
                   "slidingWindowClause", "windowStartCondition", "windowEndCondition", 
                   "windowVars", "countClause", "whereClause", "groupByClause", 
                   "groupingSpecList", "groupingSpec", "orderByClause", 
                   "orderSpec", "returnClause", "quantifiedExpr", "quantifiedVar", 
                   "switchExpr", "switchCaseClause", "switchCaseOperand", 
                   "typeswitchExpr", "caseClause", "sequenceUnionType", 
                   "ifExpr", "tryCatchExpr", "tryClause", "enclosedTryTargetExpression", 
                   "catchClause", "enclosedExpression", "catchErrorList", 
                   "existUpdateExpr", "existReplaceExpr", "existValueExpr", 
                   "existInsertExpr", "existDeleteExpr", "existRenameExpr", 
                   "orExpr", "andExpr", "comparisonExpr", "stringConcatExpr", 
                   "rangeExpr", "additiveExpr", "multiplicativeExpr", "unionExpr", 
                   "intersectExceptExpr", "instanceOfExpr", "treatExpr", 
                   "castableExpr", "castExpr", "arrowExpr", "unaryExpression", 
                   "valueExpr", "generalComp", "valueComp", "nodeComp", 
                   "validateExpr", "validationMode", "extensionExpr", "simpleMapExpr", 
                   "pathExpr", "relativePathExpr", "stepExpr", "axisStep", 
                   "forwardStep", "forwardAxis", "abbrevForwardStep", "reverseStep", 
                   "reverseAxis", "abbrevReverseStep", "nodeTest", "nameTest", 
                   "wildcard", "postfixExpr", "argumentList", "predicateList", 
                   "predicate", "lookup", "keySpecifier", "arrowFunctionSpecifier", 
                   "primaryExpr", "literal", "numericLiteral", "varRef", 
                   "varName", "parenthesizedExpr", "contextItemExpr", "orderedExpr", 
                   "unorderedExpr", "functionCall", "argument", "nodeConstructor", 
                   "directConstructor", "dirElemConstructorOpenClose", "dirElemConstructorSingleTag", 
                   "dirAttributeList", "dirAttributeValueApos", "dirAttributeValueQuot", 
                   "dirAttributeValue", "dirAttributeContentQuot", "dirAttributeContentApos", 
                   "dirElemContent", "commonContent", "computedConstructor", 
                   "compMLJSONConstructor", "compMLJSONArrayConstructor", 
                   "compMLJSONObjectConstructor", "compMLJSONNumberConstructor", 
                   "compMLJSONBooleanConstructor", "compMLJSONNullConstructor", 
                   "compBinaryConstructor", "compDocConstructor", "compElemConstructor", 
                   "enclosedContentExpr", "compAttrConstructor", "compNamespaceConstructor", 
                   "prefix", "enclosedPrefixExpr", "enclosedURIExpr", "compTextConstructor", 
                   "compCommentConstructor", "compPIConstructor", "functionItemExpr", 
                   "namedFunctionRef", "inlineFunctionRef", "functionBody", 
                   "mapConstructor", "mapConstructorEntry", "arrayConstructor", 
                   "squareArrayConstructor", "curlyArrayConstructor", "stringConstructor", 
                   "stringConstructorContent", "charNoGrave", "charNoLBrace", 
                   "charNoRBrack", "stringConstructorChars", "stringConstructorInterpolation", 
                   "unaryLookup", "singleType", "typeDeclaration", "sequenceType", 
                   "itemType", "atomicOrUnionType", "kindTest", "anyKindTest", 
                   "binaryNodeTest", "documentTest", "textTest", "commentTest", 
                   "namespaceNodeTest", "piTest", "attributeTest", "attributeNameOrWildcard", 
                   "schemaAttributeTest", "elementTest", "elementNameOrWildcard", 
                   "schemaElementTest", "elementDeclaration", "attributeName", 
                   "elementName", "simpleTypeName", "typeName", "functionTest", 
                   "anyFunctionTest", "typedFunctionTest", "mapTest", "anyMapTest", 
                   "typedMapTest", "arrayTest", "anyArrayTest", "typedArrayTest", 
                   "parenthesizedItemTest", "attributeDeclaration", "mlNodeTest", 
                   "mlArrayNodeTest", "mlObjectNodeTest", "mlNumberNodeTest", 
                   "mlBooleanNodeTest", "mlNullNodeTest", "eqName", "qName", 
                   "ncName", "functionName", "keyword", "keywordNotOKForFunction", 
                   "keywordOKForFunction", "uriLiteral", "stringLiteralQuot", 
                   "stringLiteralApos", "stringLiteral", "stringContentQuot", 
                   "stringContentApos", "noQuotesNoBracesNoAmpNoLAng" ]

    EOF = Token.EOF
    EscapeQuot=1
    EscapeApos=2
    DOUBLE_LBRACE=3
    DOUBLE_RBRACE=4
    IntegerLiteral=5
    DecimalLiteral=6
    DoubleLiteral=7
    DFPropertyName=8
    PredefinedEntityRef=9
    CharRef=10
    Quot=11
    Apos=12
    COMMENT=13
    XMLDECL=14
    PI=15
    CDATA=16
    PRAGMA=17
    WS=18
    EQUAL=19
    NOT_EQUAL=20
    LPAREN=21
    RPAREN=22
    LBRACKET=23
    RBRACKET=24
    LBRACE=25
    RBRACE=26
    STAR=27
    PLUS=28
    MINUS=29
    COMMA=30
    DOT=31
    DDOT=32
    COLON=33
    COLON_EQ=34
    SEMICOLON=35
    SLASH=36
    DSLASH=37
    BACKSLASH=38
    VBAR=39
    LANGLE=40
    RANGLE=41
    QUESTION=42
    AT=43
    DOLLAR=44
    MOD=45
    BANG=46
    HASH=47
    CARAT=48
    ARROW=49
    GRAVE=50
    CONCATENATION=51
    TILDE=52
    KW_ALLOWING=53
    KW_ANCESTOR=54
    KW_ANCESTOR_OR_SELF=55
    KW_AND=56
    KW_ARRAY=57
    KW_AS=58
    KW_ASCENDING=59
    KW_AT=60
    KW_ATTRIBUTE=61
    KW_BASE_URI=62
    KW_BOUNDARY_SPACE=63
    KW_BINARY=64
    KW_BY=65
    KW_CASE=66
    KW_CAST=67
    KW_CASTABLE=68
    KW_CATCH=69
    KW_CHILD=70
    KW_COLLATION=71
    KW_COMMENT=72
    KW_CONSTRUCTION=73
    KW_CONTEXT=74
    KW_COPY_NS=75
    KW_COUNT=76
    KW_DECLARE=77
    KW_DEFAULT=78
    KW_DESCENDANT=79
    KW_DESCENDANT_OR_SELF=80
    KW_DESCENDING=81
    KW_DECIMAL_FORMAT=82
    KW_DIV=83
    KW_DOCUMENT=84
    KW_DOCUMENT_NODE=85
    KW_ELEMENT=86
    KW_ELSE=87
    KW_EMPTY=88
    KW_EMPTY_SEQUENCE=89
    KW_ENCODING=90
    KW_END=91
    KW_EQ=92
    KW_EVERY=93
    KW_EXCEPT=94
    KW_EXTERNAL=95
    KW_FOLLOWING=96
    KW_FOLLOWING_SIBLING=97
    KW_FOR=98
    KW_FUNCTION=99
    KW_GE=100
    KW_GREATEST=101
    KW_GROUP=102
    KW_GT=103
    KW_IDIV=104
    KW_IF=105
    KW_IMPORT=106
    KW_IN=107
    KW_INHERIT=108
    KW_INSTANCE=109
    KW_INTERSECT=110
    KW_IS=111
    KW_ITEM=112
    KW_LAX=113
    KW_LE=114
    KW_LEAST=115
    KW_LET=116
    KW_LT=117
    KW_MAP=118
    KW_MOD=119
    KW_MODULE=120
    KW_NAMESPACE=121
    KW_NE=122
    KW_NEXT=123
    KW_NAMESPACE_NODE=124
    KW_NO_INHERIT=125
    KW_NO_PRESERVE=126
    KW_NODE=127
    KW_OF=128
    KW_ONLY=129
    KW_OPTION=130
    KW_OR=131
    KW_ORDER=132
    KW_ORDERED=133
    KW_ORDERING=134
    KW_PARENT=135
    KW_PRECEDING=136
    KW_PRECEDING_SIBLING=137
    KW_PRESERVE=138
    KW_PREVIOUS=139
    KW_PI=140
    KW_RETURN=141
    KW_SATISFIES=142
    KW_SCHEMA=143
    KW_SCHEMA_ATTR=144
    KW_SCHEMA_ELEM=145
    KW_SELF=146
    KW_SLIDING=147
    KW_SOME=148
    KW_STABLE=149
    KW_START=150
    KW_STRICT=151
    KW_STRIP=152
    KW_SWITCH=153
    KW_TEXT=154
    KW_THEN=155
    KW_TO=156
    KW_TREAT=157
    KW_TRY=158
    KW_TUMBLING=159
    KW_TYPE=160
    KW_TYPESWITCH=161
    KW_UNION=162
    KW_UNORDERED=163
    KW_UPDATE=164
    KW_VALIDATE=165
    KW_VARIABLE=166
    KW_VERSION=167
    KW_WHEN=168
    KW_WHERE=169
    KW_WINDOW=170
    KW_XQUERY=171
    KW_ARRAY_NODE=172
    KW_BOOLEAN_NODE=173
    KW_NULL_NODE=174
    KW_NUMBER_NODE=175
    KW_OBJECT_NODE=176
    KW_REPLACE=177
    KW_WITH=178
    KW_VALUE=179
    KW_INSERT=180
    KW_INTO=181
    KW_DELETE=182
    KW_RENAME=183
    URIQualifiedName=184
    FullQName=185
    NCNameWithLocalWildcard=186
    NCNameWithPrefixWildcard=187
    NCName=188
    XQDOC_COMMENT_START=189
    XQDOC_COMMENT_END=190
    XQDocComment=191
    XQComment=192
    CHAR=193
    ENTER_STRING=194
    EXIT_INTERPOLATION=195
    ContentChar=196
    BASIC_CHAR=197
    ENTER_INTERPOLATION=198
    EXIT_STRING=199
    EscapeQuot_QuotString=200
    DOUBLE_LBRACE_QuotString=201
    DOUBLE_RBRACE_QuotString=202
    EscapeApos_AposString=203

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ModuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def libraryModule(self):
            return self.getTypedRuleContext(XQueryParser.LibraryModuleContext,0)


        def xqDocComment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.XqDocCommentContext)
            else:
                return self.getTypedRuleContext(XQueryParser.XqDocCommentContext,i)


        def versionDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.VersionDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.VersionDeclContext,i)


        def mainModule(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.MainModuleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.MainModuleContext,i)


        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.SEMICOLON)
            else:
                return self.getToken(XQueryParser.SEMICOLON, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_module

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModule" ):
                listener.enterModule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModule" ):
                listener.exitModule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModule" ):
                return visitor.visitModule(self)
            else:
                return visitor.visitChildren(self)




    def module(self):

        localctx = XQueryParser.ModuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_module)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 481
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 480
                self.xqDocComment()


            self.state = 484
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.state = 483
                self.versionDecl()


            self.state = 487
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 486
                self.xqDocComment()


            self.state = 501
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 489
                self.libraryModule()
                pass

            elif la_ == 2:
                self.state = 490
                self.mainModule()
                self.state = 498
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.SEMICOLON:
                    self.state = 491
                    self.match(XQueryParser.SEMICOLON)
                    self.state = 493
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        self.state = 492
                        self.versionDecl()


                    self.state = 495
                    self.mainModule()
                    self.state = 500
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class XqDocCommentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def XQDocComment(self):
            return self.getToken(XQueryParser.XQDocComment, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_xqDocComment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXqDocComment" ):
                listener.enterXqDocComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXqDocComment" ):
                listener.exitXqDocComment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitXqDocComment" ):
                return visitor.visitXqDocComment(self)
            else:
                return visitor.visitChildren(self)




    def xqDocComment(self):

        localctx = XQueryParser.XqDocCommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_xqDocComment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 503
            self.match(XQueryParser.XQDocComment)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VersionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.version = None # StringLiteralContext
            self.encoding = None # StringLiteralContext

        def KW_XQUERY(self):
            return self.getToken(XQueryParser.KW_XQUERY, 0)

        def KW_VERSION(self):
            return self.getToken(XQueryParser.KW_VERSION, 0)

        def SEMICOLON(self):
            return self.getToken(XQueryParser.SEMICOLON, 0)

        def stringLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringLiteralContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringLiteralContext,i)


        def KW_ENCODING(self):
            return self.getToken(XQueryParser.KW_ENCODING, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_versionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionDecl" ):
                listener.enterVersionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionDecl" ):
                listener.exitVersionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionDecl" ):
                return visitor.visitVersionDecl(self)
            else:
                return visitor.visitChildren(self)




    def versionDecl(self):

        localctx = XQueryParser.VersionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_versionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 505
            self.match(XQueryParser.KW_XQUERY)
            self.state = 506
            self.match(XQueryParser.KW_VERSION)
            self.state = 507
            localctx.version = self.stringLiteral()
            self.state = 510
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_ENCODING:
                self.state = 508
                self.match(XQueryParser.KW_ENCODING)
                self.state = 509
                localctx.encoding = self.stringLiteral()


            self.state = 512
            self.match(XQueryParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MainModuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def prolog(self):
            return self.getTypedRuleContext(XQueryParser.PrologContext,0)


        def queryBody(self):
            return self.getTypedRuleContext(XQueryParser.QueryBodyContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mainModule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMainModule" ):
                listener.enterMainModule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMainModule" ):
                listener.exitMainModule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMainModule" ):
                return visitor.visitMainModule(self)
            else:
                return visitor.visitChildren(self)




    def mainModule(self):

        localctx = XQueryParser.MainModuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_mainModule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 514
            self.prolog()
            self.state = 515
            self.queryBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QueryBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_queryBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQueryBody" ):
                listener.enterQueryBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQueryBody" ):
                listener.exitQueryBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQueryBody" ):
                return visitor.visitQueryBody(self)
            else:
                return visitor.visitChildren(self)




    def queryBody(self):

        localctx = XQueryParser.QueryBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_queryBody)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 517
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LibraryModuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def moduleDecl(self):
            return self.getTypedRuleContext(XQueryParser.ModuleDeclContext,0)


        def prolog(self):
            return self.getTypedRuleContext(XQueryParser.PrologContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_libraryModule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLibraryModule" ):
                listener.enterLibraryModule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLibraryModule" ):
                listener.exitLibraryModule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLibraryModule" ):
                return visitor.visitLibraryModule(self)
            else:
                return visitor.visitChildren(self)




    def libraryModule(self):

        localctx = XQueryParser.LibraryModuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_libraryModule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 519
            self.moduleDecl()
            self.state = 520
            self.prolog()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.uri = None # StringLiteralContext

        def KW_MODULE(self):
            return self.getToken(XQueryParser.KW_MODULE, 0)

        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def EQUAL(self):
            return self.getToken(XQueryParser.EQUAL, 0)

        def SEMICOLON(self):
            return self.getToken(XQueryParser.SEMICOLON, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_moduleDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModuleDecl" ):
                listener.enterModuleDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModuleDecl" ):
                listener.exitModuleDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleDecl" ):
                return visitor.visitModuleDecl(self)
            else:
                return visitor.visitChildren(self)




    def moduleDecl(self):

        localctx = XQueryParser.ModuleDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_moduleDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 522
            self.match(XQueryParser.KW_MODULE)
            self.state = 523
            self.match(XQueryParser.KW_NAMESPACE)
            self.state = 524
            self.ncName()
            self.state = 525
            self.match(XQueryParser.EQUAL)
            self.state = 526
            localctx.uri = self.stringLiteral()
            self.state = 527
            self.match(XQueryParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrologContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.SEMICOLON)
            else:
                return self.getToken(XQueryParser.SEMICOLON, i)

        def defaultNamespaceDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.DefaultNamespaceDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.DefaultNamespaceDeclContext,i)


        def setter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.SetterContext)
            else:
                return self.getTypedRuleContext(XQueryParser.SetterContext,i)


        def namespaceDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.NamespaceDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.NamespaceDeclContext,i)


        def schemaImport(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.SchemaImportContext)
            else:
                return self.getTypedRuleContext(XQueryParser.SchemaImportContext,i)


        def moduleImport(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ModuleImportContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ModuleImportContext,i)


        def varDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.VarDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.VarDeclContext,i)


        def functionDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.FunctionDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.FunctionDeclContext,i)


        def contextItemDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ContextItemDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ContextItemDeclContext,i)


        def optionDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.OptionDeclContext)
            else:
                return self.getTypedRuleContext(XQueryParser.OptionDeclContext,i)


        def xqDocComment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.XqDocCommentContext)
            else:
                return self.getTypedRuleContext(XQueryParser.XqDocCommentContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_prolog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProlog" ):
                listener.enterProlog(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProlog" ):
                listener.exitProlog(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProlog" ):
                return visitor.visitProlog(self)
            else:
                return visitor.visitChildren(self)




    def prolog(self):

        localctx = XQueryParser.PrologContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_prolog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 540
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 534
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                    if la_ == 1:
                        self.state = 529
                        self.defaultNamespaceDecl()
                        pass

                    elif la_ == 2:
                        self.state = 530
                        self.setter()
                        pass

                    elif la_ == 3:
                        self.state = 531
                        self.namespaceDecl()
                        pass

                    elif la_ == 4:
                        self.state = 532
                        self.schemaImport()
                        pass

                    elif la_ == 5:
                        self.state = 533
                        self.moduleImport()
                        pass


                    self.state = 536
                    self.match(XQueryParser.SEMICOLON) 
                self.state = 542
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

            self.state = 556
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 544
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==XQueryParser.XQDocComment:
                        self.state = 543
                        self.xqDocComment()


                    self.state = 550
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
                    if la_ == 1:
                        self.state = 546
                        self.varDecl()
                        pass

                    elif la_ == 2:
                        self.state = 547
                        self.functionDecl()
                        pass

                    elif la_ == 3:
                        self.state = 548
                        self.contextItemDecl()
                        pass

                    elif la_ == 4:
                        self.state = 549
                        self.optionDecl()
                        pass


                    self.state = 552
                    self.match(XQueryParser.SEMICOLON) 
                self.state = 558
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefaultNamespaceDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.uri = None # StringLiteralContext

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def KW_ELEMENT(self):
            return self.getToken(XQueryParser.KW_ELEMENT, 0)

        def KW_FUNCTION(self):
            return self.getToken(XQueryParser.KW_FUNCTION, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_defaultNamespaceDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefaultNamespaceDecl" ):
                listener.enterDefaultNamespaceDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefaultNamespaceDecl" ):
                listener.exitDefaultNamespaceDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultNamespaceDecl" ):
                return visitor.visitDefaultNamespaceDecl(self)
            else:
                return visitor.visitChildren(self)




    def defaultNamespaceDecl(self):

        localctx = XQueryParser.DefaultNamespaceDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_defaultNamespaceDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 559
            self.match(XQueryParser.KW_DECLARE)
            self.state = 560
            self.match(XQueryParser.KW_DEFAULT)
            self.state = 561
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_ELEMENT or _la==XQueryParser.KW_FUNCTION):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 562
            self.match(XQueryParser.KW_NAMESPACE)
            self.state = 563
            localctx.uri = self.stringLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boundarySpaceDecl(self):
            return self.getTypedRuleContext(XQueryParser.BoundarySpaceDeclContext,0)


        def defaultCollationDecl(self):
            return self.getTypedRuleContext(XQueryParser.DefaultCollationDeclContext,0)


        def baseURIDecl(self):
            return self.getTypedRuleContext(XQueryParser.BaseURIDeclContext,0)


        def constructionDecl(self):
            return self.getTypedRuleContext(XQueryParser.ConstructionDeclContext,0)


        def orderingModeDecl(self):
            return self.getTypedRuleContext(XQueryParser.OrderingModeDeclContext,0)


        def emptyOrderDecl(self):
            return self.getTypedRuleContext(XQueryParser.EmptyOrderDeclContext,0)


        def copyNamespacesDecl(self):
            return self.getTypedRuleContext(XQueryParser.CopyNamespacesDeclContext,0)


        def decimalFormatDecl(self):
            return self.getTypedRuleContext(XQueryParser.DecimalFormatDeclContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_setter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetter" ):
                listener.enterSetter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetter" ):
                listener.exitSetter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetter" ):
                return visitor.visitSetter(self)
            else:
                return visitor.visitChildren(self)




    def setter(self):

        localctx = XQueryParser.SetterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_setter)
        try:
            self.state = 573
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 565
                self.boundarySpaceDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 566
                self.defaultCollationDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 567
                self.baseURIDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 568
                self.constructionDecl()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 569
                self.orderingModeDecl()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 570
                self.emptyOrderDecl()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 571
                self.copyNamespacesDecl()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 572
                self.decimalFormatDecl()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoundarySpaceDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_BOUNDARY_SPACE(self):
            return self.getToken(XQueryParser.KW_BOUNDARY_SPACE, 0)

        def KW_PRESERVE(self):
            return self.getToken(XQueryParser.KW_PRESERVE, 0)

        def KW_STRIP(self):
            return self.getToken(XQueryParser.KW_STRIP, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_boundarySpaceDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoundarySpaceDecl" ):
                listener.enterBoundarySpaceDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoundarySpaceDecl" ):
                listener.exitBoundarySpaceDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoundarySpaceDecl" ):
                return visitor.visitBoundarySpaceDecl(self)
            else:
                return visitor.visitChildren(self)




    def boundarySpaceDecl(self):

        localctx = XQueryParser.BoundarySpaceDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_boundarySpaceDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 575
            self.match(XQueryParser.KW_DECLARE)
            self.state = 576
            self.match(XQueryParser.KW_BOUNDARY_SPACE)
            self.state = 577
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_PRESERVE or _la==XQueryParser.KW_STRIP):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefaultCollationDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_COLLATION(self):
            return self.getToken(XQueryParser.KW_COLLATION, 0)

        def uriLiteral(self):
            return self.getTypedRuleContext(XQueryParser.UriLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_defaultCollationDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefaultCollationDecl" ):
                listener.enterDefaultCollationDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefaultCollationDecl" ):
                listener.exitDefaultCollationDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultCollationDecl" ):
                return visitor.visitDefaultCollationDecl(self)
            else:
                return visitor.visitChildren(self)




    def defaultCollationDecl(self):

        localctx = XQueryParser.DefaultCollationDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_defaultCollationDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 579
            self.match(XQueryParser.KW_DECLARE)
            self.state = 580
            self.match(XQueryParser.KW_DEFAULT)
            self.state = 581
            self.match(XQueryParser.KW_COLLATION)
            self.state = 582
            self.uriLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BaseURIDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_BASE_URI(self):
            return self.getToken(XQueryParser.KW_BASE_URI, 0)

        def uriLiteral(self):
            return self.getTypedRuleContext(XQueryParser.UriLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_baseURIDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBaseURIDecl" ):
                listener.enterBaseURIDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBaseURIDecl" ):
                listener.exitBaseURIDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBaseURIDecl" ):
                return visitor.visitBaseURIDecl(self)
            else:
                return visitor.visitChildren(self)




    def baseURIDecl(self):

        localctx = XQueryParser.BaseURIDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_baseURIDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 584
            self.match(XQueryParser.KW_DECLARE)
            self.state = 585
            self.match(XQueryParser.KW_BASE_URI)
            self.state = 586
            self.uriLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstructionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_CONSTRUCTION(self):
            return self.getToken(XQueryParser.KW_CONSTRUCTION, 0)

        def KW_STRIP(self):
            return self.getToken(XQueryParser.KW_STRIP, 0)

        def KW_PRESERVE(self):
            return self.getToken(XQueryParser.KW_PRESERVE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_constructionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstructionDecl" ):
                listener.enterConstructionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstructionDecl" ):
                listener.exitConstructionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstructionDecl" ):
                return visitor.visitConstructionDecl(self)
            else:
                return visitor.visitChildren(self)




    def constructionDecl(self):

        localctx = XQueryParser.ConstructionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_constructionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 588
            self.match(XQueryParser.KW_DECLARE)
            self.state = 589
            self.match(XQueryParser.KW_CONSTRUCTION)
            self.state = 590
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_PRESERVE or _la==XQueryParser.KW_STRIP):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderingModeDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_ORDERING(self):
            return self.getToken(XQueryParser.KW_ORDERING, 0)

        def KW_ORDERED(self):
            return self.getToken(XQueryParser.KW_ORDERED, 0)

        def KW_UNORDERED(self):
            return self.getToken(XQueryParser.KW_UNORDERED, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_orderingModeDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderingModeDecl" ):
                listener.enterOrderingModeDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderingModeDecl" ):
                listener.exitOrderingModeDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderingModeDecl" ):
                return visitor.visitOrderingModeDecl(self)
            else:
                return visitor.visitChildren(self)




    def orderingModeDecl(self):

        localctx = XQueryParser.OrderingModeDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_orderingModeDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 592
            self.match(XQueryParser.KW_DECLARE)
            self.state = 593
            self.match(XQueryParser.KW_ORDERING)
            self.state = 594
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_ORDERED or _la==XQueryParser.KW_UNORDERED):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EmptyOrderDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_ORDER(self):
            return self.getToken(XQueryParser.KW_ORDER, 0)

        def KW_EMPTY(self):
            return self.getToken(XQueryParser.KW_EMPTY, 0)

        def KW_GREATEST(self):
            return self.getToken(XQueryParser.KW_GREATEST, 0)

        def KW_LEAST(self):
            return self.getToken(XQueryParser.KW_LEAST, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_emptyOrderDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmptyOrderDecl" ):
                listener.enterEmptyOrderDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmptyOrderDecl" ):
                listener.exitEmptyOrderDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyOrderDecl" ):
                return visitor.visitEmptyOrderDecl(self)
            else:
                return visitor.visitChildren(self)




    def emptyOrderDecl(self):

        localctx = XQueryParser.EmptyOrderDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_emptyOrderDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 596
            self.match(XQueryParser.KW_DECLARE)
            self.state = 597
            self.match(XQueryParser.KW_DEFAULT)
            self.state = 598
            self.match(XQueryParser.KW_ORDER)
            self.state = 599
            self.match(XQueryParser.KW_EMPTY)
            self.state = 600
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_GREATEST or _la==XQueryParser.KW_LEAST):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CopyNamespacesDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_COPY_NS(self):
            return self.getToken(XQueryParser.KW_COPY_NS, 0)

        def preserveMode(self):
            return self.getTypedRuleContext(XQueryParser.PreserveModeContext,0)


        def COMMA(self):
            return self.getToken(XQueryParser.COMMA, 0)

        def inheritMode(self):
            return self.getTypedRuleContext(XQueryParser.InheritModeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_copyNamespacesDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCopyNamespacesDecl" ):
                listener.enterCopyNamespacesDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCopyNamespacesDecl" ):
                listener.exitCopyNamespacesDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCopyNamespacesDecl" ):
                return visitor.visitCopyNamespacesDecl(self)
            else:
                return visitor.visitChildren(self)




    def copyNamespacesDecl(self):

        localctx = XQueryParser.CopyNamespacesDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_copyNamespacesDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 602
            self.match(XQueryParser.KW_DECLARE)
            self.state = 603
            self.match(XQueryParser.KW_COPY_NS)
            self.state = 604
            self.preserveMode()
            self.state = 605
            self.match(XQueryParser.COMMA)
            self.state = 606
            self.inheritMode()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PreserveModeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_PRESERVE(self):
            return self.getToken(XQueryParser.KW_PRESERVE, 0)

        def KW_NO_PRESERVE(self):
            return self.getToken(XQueryParser.KW_NO_PRESERVE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_preserveMode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreserveMode" ):
                listener.enterPreserveMode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreserveMode" ):
                listener.exitPreserveMode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPreserveMode" ):
                return visitor.visitPreserveMode(self)
            else:
                return visitor.visitChildren(self)




    def preserveMode(self):

        localctx = XQueryParser.PreserveModeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_preserveMode)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 608
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_NO_PRESERVE or _la==XQueryParser.KW_PRESERVE):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InheritModeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_INHERIT(self):
            return self.getToken(XQueryParser.KW_INHERIT, 0)

        def KW_NO_INHERIT(self):
            return self.getToken(XQueryParser.KW_NO_INHERIT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_inheritMode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInheritMode" ):
                listener.enterInheritMode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInheritMode" ):
                listener.exitInheritMode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInheritMode" ):
                return visitor.visitInheritMode(self)
            else:
                return visitor.visitChildren(self)




    def inheritMode(self):

        localctx = XQueryParser.InheritModeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_inheritMode)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 610
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_INHERIT or _la==XQueryParser.KW_NO_INHERIT):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DecimalFormatDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def DFPropertyName(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DFPropertyName)
            else:
                return self.getToken(XQueryParser.DFPropertyName, i)

        def EQUAL(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EQUAL)
            else:
                return self.getToken(XQueryParser.EQUAL, i)

        def stringLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringLiteralContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringLiteralContext,i)


        def KW_DECIMAL_FORMAT(self):
            return self.getToken(XQueryParser.KW_DECIMAL_FORMAT, 0)

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_decimalFormatDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecimalFormatDecl" ):
                listener.enterDecimalFormatDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecimalFormatDecl" ):
                listener.exitDecimalFormatDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecimalFormatDecl" ):
                return visitor.visitDecimalFormatDecl(self)
            else:
                return visitor.visitChildren(self)




    def decimalFormatDecl(self):

        localctx = XQueryParser.DecimalFormatDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_decimalFormatDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 612
            self.match(XQueryParser.KW_DECLARE)
            self.state = 617
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_DECIMAL_FORMAT]:
                self.state = 613
                self.match(XQueryParser.KW_DECIMAL_FORMAT)
                self.state = 614
                self.eqName()
                pass
            elif token in [XQueryParser.KW_DEFAULT]:
                self.state = 615
                self.match(XQueryParser.KW_DEFAULT)
                self.state = 616
                self.match(XQueryParser.KW_DECIMAL_FORMAT)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 624
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.DFPropertyName:
                self.state = 619
                self.match(XQueryParser.DFPropertyName)
                self.state = 620
                self.match(XQueryParser.EQUAL)
                self.state = 621
                self.stringLiteral()
                self.state = 626
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SchemaImportContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.nsURI = None # UriLiteralContext
            self._uriLiteral = None # UriLiteralContext
            self.locations = list() # of UriLiteralContexts

        def KW_IMPORT(self):
            return self.getToken(XQueryParser.KW_IMPORT, 0)

        def KW_SCHEMA(self):
            return self.getToken(XQueryParser.KW_SCHEMA, 0)

        def uriLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.UriLiteralContext)
            else:
                return self.getTypedRuleContext(XQueryParser.UriLiteralContext,i)


        def schemaPrefix(self):
            return self.getTypedRuleContext(XQueryParser.SchemaPrefixContext,0)


        def KW_AT(self):
            return self.getToken(XQueryParser.KW_AT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_schemaImport

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSchemaImport" ):
                listener.enterSchemaImport(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSchemaImport" ):
                listener.exitSchemaImport(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSchemaImport" ):
                return visitor.visitSchemaImport(self)
            else:
                return visitor.visitChildren(self)




    def schemaImport(self):

        localctx = XQueryParser.SchemaImportContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_schemaImport)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 627
            self.match(XQueryParser.KW_IMPORT)
            self.state = 628
            self.match(XQueryParser.KW_SCHEMA)
            self.state = 630
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_DEFAULT or _la==XQueryParser.KW_NAMESPACE:
                self.state = 629
                self.schemaPrefix()


            self.state = 632
            localctx.nsURI = self.uriLiteral()
            self.state = 642
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AT:
                self.state = 633
                self.match(XQueryParser.KW_AT)
                self.state = 634
                localctx._uriLiteral = self.uriLiteral()
                localctx.locations.append(localctx._uriLiteral)
                self.state = 639
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 635
                    self.match(XQueryParser.COMMA)
                    self.state = 636
                    localctx._uriLiteral = self.uriLiteral()
                    localctx.locations.append(localctx._uriLiteral)
                    self.state = 641
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SchemaPrefixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def EQUAL(self):
            return self.getToken(XQueryParser.EQUAL, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_ELEMENT(self):
            return self.getToken(XQueryParser.KW_ELEMENT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_schemaPrefix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSchemaPrefix" ):
                listener.enterSchemaPrefix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSchemaPrefix" ):
                listener.exitSchemaPrefix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSchemaPrefix" ):
                return visitor.visitSchemaPrefix(self)
            else:
                return visitor.visitChildren(self)




    def schemaPrefix(self):

        localctx = XQueryParser.SchemaPrefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_schemaPrefix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 651
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_NAMESPACE]:
                self.state = 644
                self.match(XQueryParser.KW_NAMESPACE)
                self.state = 645
                self.ncName()
                self.state = 646
                self.match(XQueryParser.EQUAL)
                pass
            elif token in [XQueryParser.KW_DEFAULT]:
                self.state = 648
                self.match(XQueryParser.KW_DEFAULT)
                self.state = 649
                self.match(XQueryParser.KW_ELEMENT)
                self.state = 650
                self.match(XQueryParser.KW_NAMESPACE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleImportContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.nsURI = None # UriLiteralContext
            self._uriLiteral = None # UriLiteralContext
            self.locations = list() # of UriLiteralContexts

        def KW_IMPORT(self):
            return self.getToken(XQueryParser.KW_IMPORT, 0)

        def KW_MODULE(self):
            return self.getToken(XQueryParser.KW_MODULE, 0)

        def uriLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.UriLiteralContext)
            else:
                return self.getTypedRuleContext(XQueryParser.UriLiteralContext,i)


        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def EQUAL(self):
            return self.getToken(XQueryParser.EQUAL, 0)

        def KW_AT(self):
            return self.getToken(XQueryParser.KW_AT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_moduleImport

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModuleImport" ):
                listener.enterModuleImport(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModuleImport" ):
                listener.exitModuleImport(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleImport" ):
                return visitor.visitModuleImport(self)
            else:
                return visitor.visitChildren(self)




    def moduleImport(self):

        localctx = XQueryParser.ModuleImportContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_moduleImport)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 653
            self.match(XQueryParser.KW_IMPORT)
            self.state = 654
            self.match(XQueryParser.KW_MODULE)
            self.state = 659
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_NAMESPACE:
                self.state = 655
                self.match(XQueryParser.KW_NAMESPACE)
                self.state = 656
                self.ncName()
                self.state = 657
                self.match(XQueryParser.EQUAL)


            self.state = 661
            localctx.nsURI = self.uriLiteral()
            self.state = 671
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AT:
                self.state = 662
                self.match(XQueryParser.KW_AT)
                self.state = 663
                localctx._uriLiteral = self.uriLiteral()
                localctx.locations.append(localctx._uriLiteral)
                self.state = 668
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 664
                    self.match(XQueryParser.COMMA)
                    self.state = 665
                    localctx._uriLiteral = self.uriLiteral()
                    localctx.locations.append(localctx._uriLiteral)
                    self.state = 670
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamespaceDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def EQUAL(self):
            return self.getToken(XQueryParser.EQUAL, 0)

        def uriLiteral(self):
            return self.getTypedRuleContext(XQueryParser.UriLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_namespaceDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamespaceDecl" ):
                listener.enterNamespaceDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamespaceDecl" ):
                listener.exitNamespaceDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamespaceDecl" ):
                return visitor.visitNamespaceDecl(self)
            else:
                return visitor.visitChildren(self)




    def namespaceDecl(self):

        localctx = XQueryParser.NamespaceDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_namespaceDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 673
            self.match(XQueryParser.KW_DECLARE)
            self.state = 674
            self.match(XQueryParser.KW_NAMESPACE)
            self.state = 675
            self.ncName()
            self.state = 676
            self.match(XQueryParser.EQUAL)
            self.state = 677
            self.uriLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_VARIABLE(self):
            return self.getToken(XQueryParser.KW_VARIABLE, 0)

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def annotations(self):
            return self.getTypedRuleContext(XQueryParser.AnnotationsContext,0)


        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def COLON_EQ(self):
            return self.getToken(XQueryParser.COLON_EQ, 0)

        def varValue(self):
            return self.getTypedRuleContext(XQueryParser.VarValueContext,0)


        def KW_EXTERNAL(self):
            return self.getToken(XQueryParser.KW_EXTERNAL, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def varDefaultValue(self):
            return self.getTypedRuleContext(XQueryParser.VarDefaultValueContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_varDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDecl" ):
                listener.enterVarDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDecl" ):
                listener.exitVarDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDecl" ):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)




    def varDecl(self):

        localctx = XQueryParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_varDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 679
            self.match(XQueryParser.KW_DECLARE)
            self.state = 682
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.state = 680
                self.annotations()
                pass

            elif la_ == 2:
                self.state = 681
                self.ncName()
                pass


            self.state = 684
            self.match(XQueryParser.KW_VARIABLE)
            self.state = 685
            self.match(XQueryParser.DOLLAR)
            self.state = 686
            self.varName()
            self.state = 688
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 687
                self.typeDeclaration()


            self.state = 708
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
            if la_ == 1:
                self.state = 690
                self.match(XQueryParser.COLON_EQ)
                self.state = 691
                self.varValue()
                pass

            elif la_ == 2:
                self.state = 692
                self.match(XQueryParser.KW_EXTERNAL)
                self.state = 695
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==XQueryParser.COLON_EQ:
                    self.state = 693
                    self.match(XQueryParser.COLON_EQ)
                    self.state = 694
                    self.varDefaultValue()


                pass

            elif la_ == 3:
                self.state = 697
                self.match(XQueryParser.LBRACE)
                self.state = 698
                self.varValue()
                self.state = 699
                self.match(XQueryParser.RBRACE)
                pass

            elif la_ == 4:
                self.state = 701
                self.match(XQueryParser.KW_EXTERNAL)
                self.state = 706
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==XQueryParser.LBRACE:
                    self.state = 702
                    self.match(XQueryParser.LBRACE)
                    self.state = 703
                    self.varDefaultValue()
                    self.state = 704
                    self.match(XQueryParser.RBRACE)


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_varValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarValue" ):
                listener.enterVarValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarValue" ):
                listener.exitVarValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarValue" ):
                return visitor.visitVarValue(self)
            else:
                return visitor.visitChildren(self)




    def varValue(self):

        localctx = XQueryParser.VarValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_varValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 710
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDefaultValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_varDefaultValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDefaultValue" ):
                listener.enterVarDefaultValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDefaultValue" ):
                listener.exitVarDefaultValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDefaultValue" ):
                return visitor.visitVarDefaultValue(self)
            else:
                return visitor.visitChildren(self)




    def varDefaultValue(self):

        localctx = XQueryParser.VarDefaultValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_varDefaultValue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 712
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContextItemDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # ExprSingleContext
            self.defaultValue = None # ExprSingleContext

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_CONTEXT(self):
            return self.getToken(XQueryParser.KW_CONTEXT, 0)

        def KW_ITEM(self):
            return self.getToken(XQueryParser.KW_ITEM, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def itemType(self):
            return self.getTypedRuleContext(XQueryParser.ItemTypeContext,0)


        def COLON_EQ(self):
            return self.getToken(XQueryParser.COLON_EQ, 0)

        def KW_EXTERNAL(self):
            return self.getToken(XQueryParser.KW_EXTERNAL, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_contextItemDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContextItemDecl" ):
                listener.enterContextItemDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContextItemDecl" ):
                listener.exitContextItemDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContextItemDecl" ):
                return visitor.visitContextItemDecl(self)
            else:
                return visitor.visitChildren(self)




    def contextItemDecl(self):

        localctx = XQueryParser.ContextItemDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_contextItemDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 714
            self.match(XQueryParser.KW_DECLARE)
            self.state = 715
            self.match(XQueryParser.KW_CONTEXT)
            self.state = 716
            self.match(XQueryParser.KW_ITEM)
            self.state = 719
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 717
                self.match(XQueryParser.KW_AS)
                self.state = 718
                self.itemType()


            self.state = 728
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.COLON_EQ]:
                self.state = 721
                self.match(XQueryParser.COLON_EQ)
                self.state = 722
                localctx.value = self.exprSingle()
                pass
            elif token in [XQueryParser.KW_EXTERNAL]:
                self.state = 723
                self.match(XQueryParser.KW_EXTERNAL)
                self.state = 726
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==XQueryParser.COLON_EQ:
                    self.state = 724
                    self.match(XQueryParser.COLON_EQ)
                    self.state = 725
                    localctx.defaultValue = self.exprSingle()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # EqNameContext

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_FUNCTION(self):
            return self.getToken(XQueryParser.KW_FUNCTION, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def annotations(self):
            return self.getTypedRuleContext(XQueryParser.AnnotationsContext,0)


        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def functionBody(self):
            return self.getTypedRuleContext(XQueryParser.FunctionBodyContext,0)


        def KW_EXTERNAL(self):
            return self.getToken(XQueryParser.KW_EXTERNAL, 0)

        def functionParams(self):
            return self.getTypedRuleContext(XQueryParser.FunctionParamsContext,0)


        def functionReturn(self):
            return self.getTypedRuleContext(XQueryParser.FunctionReturnContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDecl" ):
                listener.enterFunctionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDecl" ):
                listener.exitFunctionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDecl" ):
                return visitor.visitFunctionDecl(self)
            else:
                return visitor.visitChildren(self)




    def functionDecl(self):

        localctx = XQueryParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_functionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 730
            self.match(XQueryParser.KW_DECLARE)
            self.state = 733
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                self.state = 731
                self.annotations()
                pass

            elif la_ == 2:
                self.state = 732
                self.ncName()
                pass


            self.state = 735
            self.match(XQueryParser.KW_FUNCTION)
            self.state = 736
            localctx.name = self.eqName()
            self.state = 737
            self.match(XQueryParser.LPAREN)
            self.state = 739
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.DOLLAR:
                self.state = 738
                self.functionParams()


            self.state = 741
            self.match(XQueryParser.RPAREN)
            self.state = 743
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 742
                self.functionReturn()


            self.state = 747
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.LBRACE]:
                self.state = 745
                self.functionBody()
                pass
            elif token in [XQueryParser.KW_EXTERNAL]:
                self.state = 746
                self.match(XQueryParser.KW_EXTERNAL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.FunctionParamContext)
            else:
                return self.getTypedRuleContext(XQueryParser.FunctionParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_functionParams

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionParams" ):
                listener.enterFunctionParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionParams" ):
                listener.exitFunctionParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionParams" ):
                return visitor.visitFunctionParams(self)
            else:
                return visitor.visitChildren(self)




    def functionParams(self):

        localctx = XQueryParser.FunctionParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_functionParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 749
            self.functionParam()
            self.state = 754
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 750
                self.match(XQueryParser.COMMA)
                self.state = 751
                self.functionParam()
                self.state = 756
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionParam

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionParam" ):
                listener.enterFunctionParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionParam" ):
                listener.exitFunctionParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionParam" ):
                return visitor.visitFunctionParam(self)
            else:
                return visitor.visitChildren(self)




    def functionParam(self):

        localctx = XQueryParser.FunctionParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_functionParam)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 757
            self.match(XQueryParser.DOLLAR)
            self.state = 758
            self.qName()
            self.state = 760
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 759
                self.typeDeclaration()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnnotationsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def annotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(XQueryParser.AnnotationContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_annotations

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnnotations" ):
                listener.enterAnnotations(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnnotations" ):
                listener.exitAnnotations(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnnotations" ):
                return visitor.visitAnnotations(self)
            else:
                return visitor.visitChildren(self)




    def annotations(self):

        localctx = XQueryParser.AnnotationsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_annotations)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 765
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.MOD:
                self.state = 762
                self.annotation()
                self.state = 767
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnnotationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MOD(self):
            return self.getToken(XQueryParser.MOD, 0)

        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def annotList(self):
            return self.getTypedRuleContext(XQueryParser.AnnotListContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_annotation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnnotation" ):
                listener.enterAnnotation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnnotation" ):
                listener.exitAnnotation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnnotation" ):
                return visitor.visitAnnotation(self)
            else:
                return visitor.visitChildren(self)




    def annotation(self):

        localctx = XQueryParser.AnnotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_annotation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 768
            self.match(XQueryParser.MOD)
            self.state = 769
            self.qName()
            self.state = 774
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.LPAREN:
                self.state = 770
                self.match(XQueryParser.LPAREN)
                self.state = 771
                self.annotList()
                self.state = 772
                self.match(XQueryParser.RPAREN)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnnotListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def annotationParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.AnnotationParamContext)
            else:
                return self.getTypedRuleContext(XQueryParser.AnnotationParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_annotList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnnotList" ):
                listener.enterAnnotList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnnotList" ):
                listener.exitAnnotList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnnotList" ):
                return visitor.visitAnnotList(self)
            else:
                return visitor.visitChildren(self)




    def annotList(self):

        localctx = XQueryParser.AnnotListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_annotList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 776
            self.annotationParam()
            self.state = 781
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 777
                self.match(XQueryParser.COMMA)
                self.state = 778
                self.annotationParam()
                self.state = 783
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnnotationParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(XQueryParser.LiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_annotationParam

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnnotationParam" ):
                listener.enterAnnotationParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnnotationParam" ):
                listener.exitAnnotationParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnnotationParam" ):
                return visitor.visitAnnotationParam(self)
            else:
                return visitor.visitChildren(self)




    def annotationParam(self):

        localctx = XQueryParser.AnnotationParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_annotationParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 784
            self.literal()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionReturnContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionReturn

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionReturn" ):
                listener.enterFunctionReturn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionReturn" ):
                listener.exitFunctionReturn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionReturn" ):
                return visitor.visitFunctionReturn(self)
            else:
                return visitor.visitChildren(self)




    def functionReturn(self):

        localctx = XQueryParser.FunctionReturnContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_functionReturn)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 786
            self.match(XQueryParser.KW_AS)
            self.state = 787
            self.sequenceType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OptionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # QNameContext
            self.value = None # StringLiteralContext

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_OPTION(self):
            return self.getToken(XQueryParser.KW_OPTION, 0)

        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_optionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOptionDecl" ):
                listener.enterOptionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOptionDecl" ):
                listener.exitOptionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOptionDecl" ):
                return visitor.visitOptionDecl(self)
            else:
                return visitor.visitChildren(self)




    def optionDecl(self):

        localctx = XQueryParser.OptionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_optionDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 789
            self.match(XQueryParser.KW_DECLARE)
            self.state = 790
            self.match(XQueryParser.KW_OPTION)
            self.state = 791
            localctx.name = self.qName()
            self.state = 792
            localctx.value = self.stringLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = XQueryParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 794
            self.exprSingle()
            self.state = 799
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,39,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 795
                    self.match(XQueryParser.COMMA)
                    self.state = 796
                    self.exprSingle() 
                self.state = 801
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,39,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprSingleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def flworExpr(self):
            return self.getTypedRuleContext(XQueryParser.FlworExprContext,0)


        def quantifiedExpr(self):
            return self.getTypedRuleContext(XQueryParser.QuantifiedExprContext,0)


        def switchExpr(self):
            return self.getTypedRuleContext(XQueryParser.SwitchExprContext,0)


        def typeswitchExpr(self):
            return self.getTypedRuleContext(XQueryParser.TypeswitchExprContext,0)


        def existUpdateExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExistUpdateExprContext,0)


        def ifExpr(self):
            return self.getTypedRuleContext(XQueryParser.IfExprContext,0)


        def tryCatchExpr(self):
            return self.getTypedRuleContext(XQueryParser.TryCatchExprContext,0)


        def orExpr(self):
            return self.getTypedRuleContext(XQueryParser.OrExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_exprSingle

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprSingle" ):
                listener.enterExprSingle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprSingle" ):
                listener.exitExprSingle(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprSingle" ):
                return visitor.visitExprSingle(self)
            else:
                return visitor.visitChildren(self)




    def exprSingle(self):

        localctx = XQueryParser.ExprSingleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_exprSingle)
        try:
            self.state = 810
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 802
                self.flworExpr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 803
                self.quantifiedExpr()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 804
                self.switchExpr()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 805
                self.typeswitchExpr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 806
                self.existUpdateExpr()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 807
                self.ifExpr()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 808
                self.tryCatchExpr()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 809
                self.orExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FlworExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def initialClause(self):
            return self.getTypedRuleContext(XQueryParser.InitialClauseContext,0)


        def returnClause(self):
            return self.getTypedRuleContext(XQueryParser.ReturnClauseContext,0)


        def intermediateClause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.IntermediateClauseContext)
            else:
                return self.getTypedRuleContext(XQueryParser.IntermediateClauseContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_flworExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFlworExpr" ):
                listener.enterFlworExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFlworExpr" ):
                listener.exitFlworExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFlworExpr" ):
                return visitor.visitFlworExpr(self)
            else:
                return visitor.visitChildren(self)




    def flworExpr(self):

        localctx = XQueryParser.FlworExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_flworExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 812
            self.initialClause()
            self.state = 816
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 76)) & ~0x3f) == 0 and ((1 << (_la - 76)) & ((1 << (XQueryParser.KW_COUNT - 76)) | (1 << (XQueryParser.KW_FOR - 76)) | (1 << (XQueryParser.KW_GROUP - 76)) | (1 << (XQueryParser.KW_LET - 76)) | (1 << (XQueryParser.KW_ORDER - 76)))) != 0) or _la==XQueryParser.KW_STABLE or _la==XQueryParser.KW_WHERE:
                self.state = 813
                self.intermediateClause()
                self.state = 818
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 819
            self.returnClause()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InitialClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def forClause(self):
            return self.getTypedRuleContext(XQueryParser.ForClauseContext,0)


        def letClause(self):
            return self.getTypedRuleContext(XQueryParser.LetClauseContext,0)


        def windowClause(self):
            return self.getTypedRuleContext(XQueryParser.WindowClauseContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_initialClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitialClause" ):
                listener.enterInitialClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitialClause" ):
                listener.exitInitialClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitialClause" ):
                return visitor.visitInitialClause(self)
            else:
                return visitor.visitChildren(self)




    def initialClause(self):

        localctx = XQueryParser.InitialClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_initialClause)
        try:
            self.state = 824
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,42,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 821
                self.forClause()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 822
                self.letClause()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 823
                self.windowClause()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntermediateClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def initialClause(self):
            return self.getTypedRuleContext(XQueryParser.InitialClauseContext,0)


        def whereClause(self):
            return self.getTypedRuleContext(XQueryParser.WhereClauseContext,0)


        def groupByClause(self):
            return self.getTypedRuleContext(XQueryParser.GroupByClauseContext,0)


        def orderByClause(self):
            return self.getTypedRuleContext(XQueryParser.OrderByClauseContext,0)


        def countClause(self):
            return self.getTypedRuleContext(XQueryParser.CountClauseContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_intermediateClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntermediateClause" ):
                listener.enterIntermediateClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntermediateClause" ):
                listener.exitIntermediateClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntermediateClause" ):
                return visitor.visitIntermediateClause(self)
            else:
                return visitor.visitChildren(self)




    def intermediateClause(self):

        localctx = XQueryParser.IntermediateClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_intermediateClause)
        try:
            self.state = 831
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_FOR, XQueryParser.KW_LET]:
                self.enterOuterAlt(localctx, 1)
                self.state = 826
                self.initialClause()
                pass
            elif token in [XQueryParser.KW_WHERE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 827
                self.whereClause()
                pass
            elif token in [XQueryParser.KW_GROUP]:
                self.enterOuterAlt(localctx, 3)
                self.state = 828
                self.groupByClause()
                pass
            elif token in [XQueryParser.KW_ORDER, XQueryParser.KW_STABLE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 829
                self.orderByClause()
                pass
            elif token in [XQueryParser.KW_COUNT]:
                self.enterOuterAlt(localctx, 5)
                self.state = 830
                self.countClause()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FOR(self):
            return self.getToken(XQueryParser.KW_FOR, 0)

        def forBinding(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ForBindingContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ForBindingContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_forClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForClause" ):
                listener.enterForClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForClause" ):
                listener.exitForClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForClause" ):
                return visitor.visitForClause(self)
            else:
                return visitor.visitChildren(self)




    def forClause(self):

        localctx = XQueryParser.ForClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_forClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 833
            self.match(XQueryParser.KW_FOR)
            self.state = 834
            self.forBinding()
            self.state = 839
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 835
                self.match(XQueryParser.COMMA)
                self.state = 836
                self.forBinding()
                self.state = 841
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForBindingContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # VarNameContext

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def KW_IN(self):
            return self.getToken(XQueryParser.KW_IN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def allowingEmpty(self):
            return self.getTypedRuleContext(XQueryParser.AllowingEmptyContext,0)


        def positionalVar(self):
            return self.getTypedRuleContext(XQueryParser.PositionalVarContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_forBinding

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForBinding" ):
                listener.enterForBinding(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForBinding" ):
                listener.exitForBinding(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForBinding" ):
                return visitor.visitForBinding(self)
            else:
                return visitor.visitChildren(self)




    def forBinding(self):

        localctx = XQueryParser.ForBindingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_forBinding)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 842
            self.match(XQueryParser.DOLLAR)
            self.state = 843
            localctx.name = self.varName()
            self.state = 845
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 844
                self.typeDeclaration()


            self.state = 848
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_ALLOWING:
                self.state = 847
                self.allowingEmpty()


            self.state = 851
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AT:
                self.state = 850
                self.positionalVar()


            self.state = 853
            self.match(XQueryParser.KW_IN)
            self.state = 854
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AllowingEmptyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ALLOWING(self):
            return self.getToken(XQueryParser.KW_ALLOWING, 0)

        def KW_EMPTY(self):
            return self.getToken(XQueryParser.KW_EMPTY, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_allowingEmpty

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAllowingEmpty" ):
                listener.enterAllowingEmpty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAllowingEmpty" ):
                listener.exitAllowingEmpty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAllowingEmpty" ):
                return visitor.visitAllowingEmpty(self)
            else:
                return visitor.visitChildren(self)




    def allowingEmpty(self):

        localctx = XQueryParser.AllowingEmptyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_allowingEmpty)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 856
            self.match(XQueryParser.KW_ALLOWING)
            self.state = 857
            self.match(XQueryParser.KW_EMPTY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PositionalVarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.pvar = None # VarNameContext

        def KW_AT(self):
            return self.getToken(XQueryParser.KW_AT, 0)

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_positionalVar

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPositionalVar" ):
                listener.enterPositionalVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPositionalVar" ):
                listener.exitPositionalVar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPositionalVar" ):
                return visitor.visitPositionalVar(self)
            else:
                return visitor.visitChildren(self)




    def positionalVar(self):

        localctx = XQueryParser.PositionalVarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_positionalVar)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 859
            self.match(XQueryParser.KW_AT)
            self.state = 860
            self.match(XQueryParser.DOLLAR)
            self.state = 861
            localctx.pvar = self.varName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LET(self):
            return self.getToken(XQueryParser.KW_LET, 0)

        def letBinding(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.LetBindingContext)
            else:
                return self.getTypedRuleContext(XQueryParser.LetBindingContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_letClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetClause" ):
                listener.enterLetClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetClause" ):
                listener.exitLetClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetClause" ):
                return visitor.visitLetClause(self)
            else:
                return visitor.visitChildren(self)




    def letClause(self):

        localctx = XQueryParser.LetClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_letClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 863
            self.match(XQueryParser.KW_LET)
            self.state = 864
            self.letBinding()
            self.state = 869
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 865
                self.match(XQueryParser.COMMA)
                self.state = 866
                self.letBinding()
                self.state = 871
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetBindingContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def COLON_EQ(self):
            return self.getToken(XQueryParser.COLON_EQ, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_letBinding

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetBinding" ):
                listener.enterLetBinding(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetBinding" ):
                listener.exitLetBinding(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetBinding" ):
                return visitor.visitLetBinding(self)
            else:
                return visitor.visitChildren(self)




    def letBinding(self):

        localctx = XQueryParser.LetBindingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_letBinding)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 872
            self.match(XQueryParser.DOLLAR)
            self.state = 873
            self.varName()
            self.state = 875
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 874
                self.typeDeclaration()


            self.state = 877
            self.match(XQueryParser.COLON_EQ)
            self.state = 878
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WindowClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FOR(self):
            return self.getToken(XQueryParser.KW_FOR, 0)

        def tumblingWindowClause(self):
            return self.getTypedRuleContext(XQueryParser.TumblingWindowClauseContext,0)


        def slidingWindowClause(self):
            return self.getTypedRuleContext(XQueryParser.SlidingWindowClauseContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_windowClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWindowClause" ):
                listener.enterWindowClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWindowClause" ):
                listener.exitWindowClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWindowClause" ):
                return visitor.visitWindowClause(self)
            else:
                return visitor.visitChildren(self)




    def windowClause(self):

        localctx = XQueryParser.WindowClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_windowClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 880
            self.match(XQueryParser.KW_FOR)
            self.state = 883
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_TUMBLING]:
                self.state = 881
                self.tumblingWindowClause()
                pass
            elif token in [XQueryParser.KW_SLIDING]:
                self.state = 882
                self.slidingWindowClause()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TumblingWindowClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # QNameContext

        def KW_TUMBLING(self):
            return self.getToken(XQueryParser.KW_TUMBLING, 0)

        def KW_WINDOW(self):
            return self.getToken(XQueryParser.KW_WINDOW, 0)

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def KW_IN(self):
            return self.getToken(XQueryParser.KW_IN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def windowStartCondition(self):
            return self.getTypedRuleContext(XQueryParser.WindowStartConditionContext,0)


        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def windowEndCondition(self):
            return self.getTypedRuleContext(XQueryParser.WindowEndConditionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_tumblingWindowClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTumblingWindowClause" ):
                listener.enterTumblingWindowClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTumblingWindowClause" ):
                listener.exitTumblingWindowClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTumblingWindowClause" ):
                return visitor.visitTumblingWindowClause(self)
            else:
                return visitor.visitChildren(self)




    def tumblingWindowClause(self):

        localctx = XQueryParser.TumblingWindowClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_tumblingWindowClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 885
            self.match(XQueryParser.KW_TUMBLING)
            self.state = 886
            self.match(XQueryParser.KW_WINDOW)
            self.state = 887
            self.match(XQueryParser.DOLLAR)
            self.state = 888
            localctx.name = self.qName()
            self.state = 890
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 889
                self.typeDeclaration()


            self.state = 892
            self.match(XQueryParser.KW_IN)
            self.state = 893
            self.exprSingle()
            self.state = 894
            self.windowStartCondition()
            self.state = 896
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_END or _la==XQueryParser.KW_ONLY:
                self.state = 895
                self.windowEndCondition()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SlidingWindowClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # QNameContext

        def KW_SLIDING(self):
            return self.getToken(XQueryParser.KW_SLIDING, 0)

        def KW_WINDOW(self):
            return self.getToken(XQueryParser.KW_WINDOW, 0)

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def KW_IN(self):
            return self.getToken(XQueryParser.KW_IN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def windowStartCondition(self):
            return self.getTypedRuleContext(XQueryParser.WindowStartConditionContext,0)


        def windowEndCondition(self):
            return self.getTypedRuleContext(XQueryParser.WindowEndConditionContext,0)


        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_slidingWindowClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSlidingWindowClause" ):
                listener.enterSlidingWindowClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSlidingWindowClause" ):
                listener.exitSlidingWindowClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSlidingWindowClause" ):
                return visitor.visitSlidingWindowClause(self)
            else:
                return visitor.visitChildren(self)




    def slidingWindowClause(self):

        localctx = XQueryParser.SlidingWindowClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_slidingWindowClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 898
            self.match(XQueryParser.KW_SLIDING)
            self.state = 899
            self.match(XQueryParser.KW_WINDOW)
            self.state = 900
            self.match(XQueryParser.DOLLAR)
            self.state = 901
            localctx.name = self.qName()
            self.state = 903
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 902
                self.typeDeclaration()


            self.state = 905
            self.match(XQueryParser.KW_IN)
            self.state = 906
            self.exprSingle()
            self.state = 907
            self.windowStartCondition()
            self.state = 908
            self.windowEndCondition()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WindowStartConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_START(self):
            return self.getToken(XQueryParser.KW_START, 0)

        def windowVars(self):
            return self.getTypedRuleContext(XQueryParser.WindowVarsContext,0)


        def KW_WHEN(self):
            return self.getToken(XQueryParser.KW_WHEN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_windowStartCondition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWindowStartCondition" ):
                listener.enterWindowStartCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWindowStartCondition" ):
                listener.exitWindowStartCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWindowStartCondition" ):
                return visitor.visitWindowStartCondition(self)
            else:
                return visitor.visitChildren(self)




    def windowStartCondition(self):

        localctx = XQueryParser.WindowStartConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_windowStartCondition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 910
            self.match(XQueryParser.KW_START)
            self.state = 911
            self.windowVars()
            self.state = 912
            self.match(XQueryParser.KW_WHEN)
            self.state = 913
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WindowEndConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_END(self):
            return self.getToken(XQueryParser.KW_END, 0)

        def windowVars(self):
            return self.getTypedRuleContext(XQueryParser.WindowVarsContext,0)


        def KW_WHEN(self):
            return self.getToken(XQueryParser.KW_WHEN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def KW_ONLY(self):
            return self.getToken(XQueryParser.KW_ONLY, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_windowEndCondition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWindowEndCondition" ):
                listener.enterWindowEndCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWindowEndCondition" ):
                listener.exitWindowEndCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWindowEndCondition" ):
                return visitor.visitWindowEndCondition(self)
            else:
                return visitor.visitChildren(self)




    def windowEndCondition(self):

        localctx = XQueryParser.WindowEndConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_windowEndCondition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 916
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_ONLY:
                self.state = 915
                self.match(XQueryParser.KW_ONLY)


            self.state = 918
            self.match(XQueryParser.KW_END)
            self.state = 919
            self.windowVars()
            self.state = 920
            self.match(XQueryParser.KW_WHEN)
            self.state = 921
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WindowVarsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.currentItem = None # EqNameContext
            self.previousItem = None # EqNameContext
            self.nextItem = None # EqNameContext

        def DOLLAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DOLLAR)
            else:
                return self.getToken(XQueryParser.DOLLAR, i)

        def positionalVar(self):
            return self.getTypedRuleContext(XQueryParser.PositionalVarContext,0)


        def KW_PREVIOUS(self):
            return self.getToken(XQueryParser.KW_PREVIOUS, 0)

        def KW_NEXT(self):
            return self.getToken(XQueryParser.KW_NEXT, 0)

        def eqName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.EqNameContext)
            else:
                return self.getTypedRuleContext(XQueryParser.EqNameContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_windowVars

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWindowVars" ):
                listener.enterWindowVars(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWindowVars" ):
                listener.exitWindowVars(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWindowVars" ):
                return visitor.visitWindowVars(self)
            else:
                return visitor.visitChildren(self)




    def windowVars(self):

        localctx = XQueryParser.WindowVarsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_windowVars)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 925
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.DOLLAR:
                self.state = 923
                self.match(XQueryParser.DOLLAR)
                self.state = 924
                localctx.currentItem = self.eqName()


            self.state = 928
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AT:
                self.state = 927
                self.positionalVar()


            self.state = 933
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_PREVIOUS:
                self.state = 930
                self.match(XQueryParser.KW_PREVIOUS)
                self.state = 931
                self.match(XQueryParser.DOLLAR)
                self.state = 932
                localctx.previousItem = self.eqName()


            self.state = 938
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_NEXT:
                self.state = 935
                self.match(XQueryParser.KW_NEXT)
                self.state = 936
                self.match(XQueryParser.DOLLAR)
                self.state = 937
                localctx.nextItem = self.eqName()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CountClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_COUNT(self):
            return self.getToken(XQueryParser.KW_COUNT, 0)

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_countClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCountClause" ):
                listener.enterCountClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCountClause" ):
                listener.exitCountClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCountClause" ):
                return visitor.visitCountClause(self)
            else:
                return visitor.visitChildren(self)




    def countClause(self):

        localctx = XQueryParser.CountClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_countClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 940
            self.match(XQueryParser.KW_COUNT)
            self.state = 941
            self.match(XQueryParser.DOLLAR)
            self.state = 942
            self.varName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.whereExpr = None # ExprSingleContext

        def KW_WHERE(self):
            return self.getToken(XQueryParser.KW_WHERE, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_whereClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhereClause" ):
                listener.enterWhereClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhereClause" ):
                listener.exitWhereClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereClause" ):
                return visitor.visitWhereClause(self)
            else:
                return visitor.visitChildren(self)




    def whereClause(self):

        localctx = XQueryParser.WhereClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_whereClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 944
            self.match(XQueryParser.KW_WHERE)
            self.state = 945
            localctx.whereExpr = self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupByClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_GROUP(self):
            return self.getToken(XQueryParser.KW_GROUP, 0)

        def KW_BY(self):
            return self.getToken(XQueryParser.KW_BY, 0)

        def groupingSpecList(self):
            return self.getTypedRuleContext(XQueryParser.GroupingSpecListContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_groupByClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupByClause" ):
                listener.enterGroupByClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupByClause" ):
                listener.exitGroupByClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupByClause" ):
                return visitor.visitGroupByClause(self)
            else:
                return visitor.visitChildren(self)




    def groupByClause(self):

        localctx = XQueryParser.GroupByClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_groupByClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 947
            self.match(XQueryParser.KW_GROUP)
            self.state = 948
            self.match(XQueryParser.KW_BY)
            self.state = 949
            self.groupingSpecList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupingSpecListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def groupingSpec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.GroupingSpecContext)
            else:
                return self.getTypedRuleContext(XQueryParser.GroupingSpecContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_groupingSpecList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupingSpecList" ):
                listener.enterGroupingSpecList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupingSpecList" ):
                listener.exitGroupingSpecList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupingSpecList" ):
                return visitor.visitGroupingSpecList(self)
            else:
                return visitor.visitChildren(self)




    def groupingSpecList(self):

        localctx = XQueryParser.GroupingSpecListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 114, self.RULE_groupingSpecList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 951
            self.groupingSpec()
            self.state = 956
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 952
                self.match(XQueryParser.COMMA)
                self.state = 953
                self.groupingSpec()
                self.state = 958
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupingSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # VarNameContext
            self.uri = None # UriLiteralContext

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def COLON_EQ(self):
            return self.getToken(XQueryParser.COLON_EQ, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def KW_COLLATION(self):
            return self.getToken(XQueryParser.KW_COLLATION, 0)

        def uriLiteral(self):
            return self.getTypedRuleContext(XQueryParser.UriLiteralContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_groupingSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupingSpec" ):
                listener.enterGroupingSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupingSpec" ):
                listener.exitGroupingSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupingSpec" ):
                return visitor.visitGroupingSpec(self)
            else:
                return visitor.visitChildren(self)




    def groupingSpec(self):

        localctx = XQueryParser.GroupingSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 116, self.RULE_groupingSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 959
            self.match(XQueryParser.DOLLAR)
            self.state = 960
            localctx.name = self.varName()
            self.state = 966
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.COLON_EQ or _la==XQueryParser.KW_AS:
                self.state = 962
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==XQueryParser.KW_AS:
                    self.state = 961
                    self.typeDeclaration()


                self.state = 964
                self.match(XQueryParser.COLON_EQ)
                self.state = 965
                self.exprSingle()


            self.state = 970
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_COLLATION:
                self.state = 968
                self.match(XQueryParser.KW_COLLATION)
                self.state = 969
                localctx.uri = self.uriLiteral()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderByClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._orderSpec = None # OrderSpecContext
            self.specs = list() # of OrderSpecContexts

        def KW_ORDER(self):
            return self.getToken(XQueryParser.KW_ORDER, 0)

        def KW_BY(self):
            return self.getToken(XQueryParser.KW_BY, 0)

        def orderSpec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.OrderSpecContext)
            else:
                return self.getTypedRuleContext(XQueryParser.OrderSpecContext,i)


        def KW_STABLE(self):
            return self.getToken(XQueryParser.KW_STABLE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_orderByClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderByClause" ):
                listener.enterOrderByClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderByClause" ):
                listener.exitOrderByClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderByClause" ):
                return visitor.visitOrderByClause(self)
            else:
                return visitor.visitChildren(self)




    def orderByClause(self):

        localctx = XQueryParser.OrderByClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 118, self.RULE_orderByClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 973
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_STABLE:
                self.state = 972
                self.match(XQueryParser.KW_STABLE)


            self.state = 975
            self.match(XQueryParser.KW_ORDER)
            self.state = 976
            self.match(XQueryParser.KW_BY)
            self.state = 977
            localctx._orderSpec = self.orderSpec()
            localctx.specs.append(localctx._orderSpec)
            self.state = 982
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 978
                self.match(XQueryParser.COMMA)
                self.state = 979
                localctx._orderSpec = self.orderSpec()
                localctx.specs.append(localctx._orderSpec)
                self.state = 984
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # ExprSingleContext
            self.order = None # Token
            self.empty = None # Token
            self.collation = None # UriLiteralContext

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def KW_EMPTY(self):
            return self.getToken(XQueryParser.KW_EMPTY, 0)

        def KW_COLLATION(self):
            return self.getToken(XQueryParser.KW_COLLATION, 0)

        def uriLiteral(self):
            return self.getTypedRuleContext(XQueryParser.UriLiteralContext,0)


        def KW_ASCENDING(self):
            return self.getToken(XQueryParser.KW_ASCENDING, 0)

        def KW_DESCENDING(self):
            return self.getToken(XQueryParser.KW_DESCENDING, 0)

        def KW_GREATEST(self):
            return self.getToken(XQueryParser.KW_GREATEST, 0)

        def KW_LEAST(self):
            return self.getToken(XQueryParser.KW_LEAST, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_orderSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderSpec" ):
                listener.enterOrderSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderSpec" ):
                listener.exitOrderSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderSpec" ):
                return visitor.visitOrderSpec(self)
            else:
                return visitor.visitChildren(self)




    def orderSpec(self):

        localctx = XQueryParser.OrderSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 120, self.RULE_orderSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 985
            localctx.value = self.exprSingle()
            self.state = 987
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_ASCENDING or _la==XQueryParser.KW_DESCENDING:
                self.state = 986
                localctx.order = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==XQueryParser.KW_ASCENDING or _la==XQueryParser.KW_DESCENDING):
                    localctx.order = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 991
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_EMPTY:
                self.state = 989
                self.match(XQueryParser.KW_EMPTY)
                self.state = 990
                localctx.empty = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==XQueryParser.KW_GREATEST or _la==XQueryParser.KW_LEAST):
                    localctx.empty = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 995
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_COLLATION:
                self.state = 993
                self.match(XQueryParser.KW_COLLATION)
                self.state = 994
                localctx.collation = self.uriLiteral()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_RETURN(self):
            return self.getToken(XQueryParser.KW_RETURN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_returnClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnClause" ):
                listener.enterReturnClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnClause" ):
                listener.exitReturnClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnClause" ):
                return visitor.visitReturnClause(self)
            else:
                return visitor.visitChildren(self)




    def returnClause(self):

        localctx = XQueryParser.ReturnClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 122, self.RULE_returnClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 997
            self.match(XQueryParser.KW_RETURN)
            self.state = 998
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantifiedExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.quantifier = None # Token
            self.value = None # ExprSingleContext

        def quantifiedVar(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.QuantifiedVarContext)
            else:
                return self.getTypedRuleContext(XQueryParser.QuantifiedVarContext,i)


        def KW_SATISFIES(self):
            return self.getToken(XQueryParser.KW_SATISFIES, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def KW_SOME(self):
            return self.getToken(XQueryParser.KW_SOME, 0)

        def KW_EVERY(self):
            return self.getToken(XQueryParser.KW_EVERY, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_quantifiedExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantifiedExpr" ):
                listener.enterQuantifiedExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantifiedExpr" ):
                listener.exitQuantifiedExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuantifiedExpr" ):
                return visitor.visitQuantifiedExpr(self)
            else:
                return visitor.visitChildren(self)




    def quantifiedExpr(self):

        localctx = XQueryParser.QuantifiedExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 124, self.RULE_quantifiedExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1000
            localctx.quantifier = self._input.LT(1)
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_EVERY or _la==XQueryParser.KW_SOME):
                localctx.quantifier = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1001
            self.quantifiedVar()
            self.state = 1006
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.COMMA:
                self.state = 1002
                self.match(XQueryParser.COMMA)
                self.state = 1003
                self.quantifiedVar()
                self.state = 1008
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1009
            self.match(XQueryParser.KW_SATISFIES)
            self.state = 1010
            localctx.value = self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantifiedVarContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def KW_IN(self):
            return self.getToken(XQueryParser.KW_IN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def typeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.TypeDeclarationContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_quantifiedVar

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantifiedVar" ):
                listener.enterQuantifiedVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantifiedVar" ):
                listener.exitQuantifiedVar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuantifiedVar" ):
                return visitor.visitQuantifiedVar(self)
            else:
                return visitor.visitChildren(self)




    def quantifiedVar(self):

        localctx = XQueryParser.QuantifiedVarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 126, self.RULE_quantifiedVar)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1012
            self.match(XQueryParser.DOLLAR)
            self.state = 1013
            self.varName()
            self.state = 1015
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 1014
                self.typeDeclaration()


            self.state = 1017
            self.match(XQueryParser.KW_IN)
            self.state = 1018
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SwitchExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.returnExpr = None # ExprSingleContext

        def KW_SWITCH(self):
            return self.getToken(XQueryParser.KW_SWITCH, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_RETURN(self):
            return self.getToken(XQueryParser.KW_RETURN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def switchCaseClause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.SwitchCaseClauseContext)
            else:
                return self.getTypedRuleContext(XQueryParser.SwitchCaseClauseContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_switchExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSwitchExpr" ):
                listener.enterSwitchExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSwitchExpr" ):
                listener.exitSwitchExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSwitchExpr" ):
                return visitor.visitSwitchExpr(self)
            else:
                return visitor.visitChildren(self)




    def switchExpr(self):

        localctx = XQueryParser.SwitchExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 128, self.RULE_switchExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1020
            self.match(XQueryParser.KW_SWITCH)
            self.state = 1021
            self.match(XQueryParser.LPAREN)
            self.state = 1022
            self.expr()
            self.state = 1023
            self.match(XQueryParser.RPAREN)
            self.state = 1025 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1024
                self.switchCaseClause()
                self.state = 1027 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==XQueryParser.KW_CASE):
                    break

            self.state = 1029
            self.match(XQueryParser.KW_DEFAULT)
            self.state = 1030
            self.match(XQueryParser.KW_RETURN)
            self.state = 1031
            localctx.returnExpr = self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SwitchCaseClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_RETURN(self):
            return self.getToken(XQueryParser.KW_RETURN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def KW_CASE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_CASE)
            else:
                return self.getToken(XQueryParser.KW_CASE, i)

        def switchCaseOperand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.SwitchCaseOperandContext)
            else:
                return self.getTypedRuleContext(XQueryParser.SwitchCaseOperandContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_switchCaseClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSwitchCaseClause" ):
                listener.enterSwitchCaseClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSwitchCaseClause" ):
                listener.exitSwitchCaseClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSwitchCaseClause" ):
                return visitor.visitSwitchCaseClause(self)
            else:
                return visitor.visitChildren(self)




    def switchCaseClause(self):

        localctx = XQueryParser.SwitchCaseClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 130, self.RULE_switchCaseClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1035 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1033
                self.match(XQueryParser.KW_CASE)
                self.state = 1034
                self.switchCaseOperand()
                self.state = 1037 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==XQueryParser.KW_CASE):
                    break

            self.state = 1039
            self.match(XQueryParser.KW_RETURN)
            self.state = 1040
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SwitchCaseOperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_switchCaseOperand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSwitchCaseOperand" ):
                listener.enterSwitchCaseOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSwitchCaseOperand" ):
                listener.exitSwitchCaseOperand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSwitchCaseOperand" ):
                return visitor.visitSwitchCaseOperand(self)
            else:
                return visitor.visitChildren(self)




    def switchCaseOperand(self):

        localctx = XQueryParser.SwitchCaseOperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 132, self.RULE_switchCaseOperand)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1042
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeswitchExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.clauses = None # CaseClauseContext
            self.var = None # VarNameContext
            self.returnExpr = None # ExprSingleContext

        def KW_TYPESWITCH(self):
            return self.getToken(XQueryParser.KW_TYPESWITCH, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_RETURN(self):
            return self.getToken(XQueryParser.KW_RETURN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def caseClause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.CaseClauseContext)
            else:
                return self.getTypedRuleContext(XQueryParser.CaseClauseContext,i)


        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_typeswitchExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeswitchExpr" ):
                listener.enterTypeswitchExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeswitchExpr" ):
                listener.exitTypeswitchExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeswitchExpr" ):
                return visitor.visitTypeswitchExpr(self)
            else:
                return visitor.visitChildren(self)




    def typeswitchExpr(self):

        localctx = XQueryParser.TypeswitchExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 134, self.RULE_typeswitchExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1044
            self.match(XQueryParser.KW_TYPESWITCH)
            self.state = 1045
            self.match(XQueryParser.LPAREN)
            self.state = 1046
            self.expr()
            self.state = 1047
            self.match(XQueryParser.RPAREN)
            self.state = 1049 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1048
                localctx.clauses = self.caseClause()
                self.state = 1051 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==XQueryParser.KW_CASE):
                    break

            self.state = 1053
            self.match(XQueryParser.KW_DEFAULT)
            self.state = 1056
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.DOLLAR:
                self.state = 1054
                self.match(XQueryParser.DOLLAR)
                self.state = 1055
                localctx.var = self.varName()


            self.state = 1058
            self.match(XQueryParser.KW_RETURN)
            self.state = 1059
            localctx.returnExpr = self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_CASE(self):
            return self.getToken(XQueryParser.KW_CASE, 0)

        def sequenceUnionType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceUnionTypeContext,0)


        def KW_RETURN(self):
            return self.getToken(XQueryParser.KW_RETURN, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_caseClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseClause" ):
                listener.enterCaseClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseClause" ):
                listener.exitCaseClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseClause" ):
                return visitor.visitCaseClause(self)
            else:
                return visitor.visitChildren(self)




    def caseClause(self):

        localctx = XQueryParser.CaseClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 136, self.RULE_caseClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1061
            self.match(XQueryParser.KW_CASE)
            self.state = 1066
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.DOLLAR:
                self.state = 1062
                self.match(XQueryParser.DOLLAR)
                self.state = 1063
                self.varName()
                self.state = 1064
                self.match(XQueryParser.KW_AS)


            self.state = 1068
            self.sequenceUnionType()
            self.state = 1069
            self.match(XQueryParser.KW_RETURN)
            self.state = 1070
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SequenceUnionTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sequenceType(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.SequenceTypeContext)
            else:
                return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,i)


        def VBAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.VBAR)
            else:
                return self.getToken(XQueryParser.VBAR, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_sequenceUnionType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSequenceUnionType" ):
                listener.enterSequenceUnionType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSequenceUnionType" ):
                listener.exitSequenceUnionType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSequenceUnionType" ):
                return visitor.visitSequenceUnionType(self)
            else:
                return visitor.visitChildren(self)




    def sequenceUnionType(self):

        localctx = XQueryParser.SequenceUnionTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 138, self.RULE_sequenceUnionType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1072
            self.sequenceType()
            self.state = 1077
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.VBAR:
                self.state = 1073
                self.match(XQueryParser.VBAR)
                self.state = 1074
                self.sequenceType()
                self.state = 1079
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.conditionExpr = None # ExprContext
            self.thenExpr = None # ExprSingleContext
            self.elseExpr = None # ExprSingleContext

        def KW_IF(self):
            return self.getToken(XQueryParser.KW_IF, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def KW_THEN(self):
            return self.getToken(XQueryParser.KW_THEN, 0)

        def KW_ELSE(self):
            return self.getToken(XQueryParser.KW_ELSE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_ifExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfExpr" ):
                listener.enterIfExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfExpr" ):
                listener.exitIfExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfExpr" ):
                return visitor.visitIfExpr(self)
            else:
                return visitor.visitChildren(self)




    def ifExpr(self):

        localctx = XQueryParser.IfExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 140, self.RULE_ifExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1080
            self.match(XQueryParser.KW_IF)
            self.state = 1081
            self.match(XQueryParser.LPAREN)
            self.state = 1082
            localctx.conditionExpr = self.expr()
            self.state = 1083
            self.match(XQueryParser.RPAREN)
            self.state = 1084
            self.match(XQueryParser.KW_THEN)
            self.state = 1085
            localctx.thenExpr = self.exprSingle()
            self.state = 1086
            self.match(XQueryParser.KW_ELSE)
            self.state = 1087
            localctx.elseExpr = self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TryCatchExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tryClause(self):
            return self.getTypedRuleContext(XQueryParser.TryClauseContext,0)


        def catchClause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.CatchClauseContext)
            else:
                return self.getTypedRuleContext(XQueryParser.CatchClauseContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_tryCatchExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTryCatchExpr" ):
                listener.enterTryCatchExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTryCatchExpr" ):
                listener.exitTryCatchExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryCatchExpr" ):
                return visitor.visitTryCatchExpr(self)
            else:
                return visitor.visitChildren(self)




    def tryCatchExpr(self):

        localctx = XQueryParser.TryCatchExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 142, self.RULE_tryCatchExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1089
            self.tryClause()
            self.state = 1091 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 1090
                    self.catchClause()

                else:
                    raise NoViableAltException(self)
                self.state = 1093 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,76,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TryClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_TRY(self):
            return self.getToken(XQueryParser.KW_TRY, 0)

        def enclosedTryTargetExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedTryTargetExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_tryClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTryClause" ):
                listener.enterTryClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTryClause" ):
                listener.exitTryClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTryClause" ):
                return visitor.visitTryClause(self)
            else:
                return visitor.visitChildren(self)




    def tryClause(self):

        localctx = XQueryParser.TryClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 144, self.RULE_tryClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1095
            self.match(XQueryParser.KW_TRY)
            self.state = 1096
            self.enclosedTryTargetExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnclosedTryTargetExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_enclosedTryTargetExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnclosedTryTargetExpression" ):
                listener.enterEnclosedTryTargetExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnclosedTryTargetExpression" ):
                listener.exitEnclosedTryTargetExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnclosedTryTargetExpression" ):
                return visitor.visitEnclosedTryTargetExpression(self)
            else:
                return visitor.visitChildren(self)




    def enclosedTryTargetExpression(self):

        localctx = XQueryParser.EnclosedTryTargetExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 146, self.RULE_enclosedTryTargetExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1098
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CatchClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_CATCH(self):
            return self.getToken(XQueryParser.KW_CATCH, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def catchErrorList(self):
            return self.getTypedRuleContext(XQueryParser.CatchErrorListContext,0)


        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def varName(self):
            return self.getTypedRuleContext(XQueryParser.VarNameContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_catchClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCatchClause" ):
                listener.enterCatchClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCatchClause" ):
                listener.exitCatchClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCatchClause" ):
                return visitor.visitCatchClause(self)
            else:
                return visitor.visitChildren(self)




    def catchClause(self):

        localctx = XQueryParser.CatchClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 148, self.RULE_catchClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1100
            self.match(XQueryParser.KW_CATCH)
            self.state = 1107
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.STAR, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCNameWithLocalWildcard, XQueryParser.NCNameWithPrefixWildcard, XQueryParser.NCName]:
                self.state = 1101
                self.catchErrorList()
                pass
            elif token in [XQueryParser.LPAREN]:
                self.state = 1102
                self.match(XQueryParser.LPAREN)
                self.state = 1103
                self.match(XQueryParser.DOLLAR)
                self.state = 1104
                self.varName()
                self.state = 1105
                self.match(XQueryParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 1109
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnclosedExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_enclosedExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnclosedExpression" ):
                listener.enterEnclosedExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnclosedExpression" ):
                listener.exitEnclosedExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnclosedExpression" ):
                return visitor.visitEnclosedExpression(self)
            else:
                return visitor.visitChildren(self)




    def enclosedExpression(self):

        localctx = XQueryParser.EnclosedExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 150, self.RULE_enclosedExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1111
            self.match(XQueryParser.LBRACE)
            self.state = 1113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                self.state = 1112
                self.expr()


            self.state = 1115
            self.match(XQueryParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CatchErrorListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def nameTest(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.NameTestContext)
            else:
                return self.getTypedRuleContext(XQueryParser.NameTestContext,i)


        def VBAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.VBAR)
            else:
                return self.getToken(XQueryParser.VBAR, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_catchErrorList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCatchErrorList" ):
                listener.enterCatchErrorList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCatchErrorList" ):
                listener.exitCatchErrorList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCatchErrorList" ):
                return visitor.visitCatchErrorList(self)
            else:
                return visitor.visitChildren(self)




    def catchErrorList(self):

        localctx = XQueryParser.CatchErrorListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 152, self.RULE_catchErrorList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1117
            self.nameTest()
            self.state = 1122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.VBAR:
                self.state = 1118
                self.match(XQueryParser.VBAR)
                self.state = 1119
                self.nameTest()
                self.state = 1124
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistUpdateExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_UPDATE(self):
            return self.getToken(XQueryParser.KW_UPDATE, 0)

        def existReplaceExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExistReplaceExprContext,0)


        def existValueExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExistValueExprContext,0)


        def existInsertExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExistInsertExprContext,0)


        def existDeleteExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExistDeleteExprContext,0)


        def existRenameExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExistRenameExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_existUpdateExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistUpdateExpr" ):
                listener.enterExistUpdateExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistUpdateExpr" ):
                listener.exitExistUpdateExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistUpdateExpr" ):
                return visitor.visitExistUpdateExpr(self)
            else:
                return visitor.visitChildren(self)




    def existUpdateExpr(self):

        localctx = XQueryParser.ExistUpdateExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 154, self.RULE_existUpdateExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1125
            self.match(XQueryParser.KW_UPDATE)
            self.state = 1131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_REPLACE]:
                self.state = 1126
                self.existReplaceExpr()
                pass
            elif token in [XQueryParser.KW_VALUE]:
                self.state = 1127
                self.existValueExpr()
                pass
            elif token in [XQueryParser.KW_INSERT]:
                self.state = 1128
                self.existInsertExpr()
                pass
            elif token in [XQueryParser.KW_DELETE]:
                self.state = 1129
                self.existDeleteExpr()
                pass
            elif token in [XQueryParser.KW_RENAME]:
                self.state = 1130
                self.existRenameExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistReplaceExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_REPLACE(self):
            return self.getToken(XQueryParser.KW_REPLACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def KW_WITH(self):
            return self.getToken(XQueryParser.KW_WITH, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_existReplaceExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistReplaceExpr" ):
                listener.enterExistReplaceExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistReplaceExpr" ):
                listener.exitExistReplaceExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistReplaceExpr" ):
                return visitor.visitExistReplaceExpr(self)
            else:
                return visitor.visitChildren(self)




    def existReplaceExpr(self):

        localctx = XQueryParser.ExistReplaceExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 156, self.RULE_existReplaceExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1133
            self.match(XQueryParser.KW_REPLACE)
            self.state = 1134
            self.expr()
            self.state = 1135
            self.match(XQueryParser.KW_WITH)
            self.state = 1136
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistValueExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_VALUE(self):
            return self.getToken(XQueryParser.KW_VALUE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def KW_WITH(self):
            return self.getToken(XQueryParser.KW_WITH, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_existValueExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistValueExpr" ):
                listener.enterExistValueExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistValueExpr" ):
                listener.exitExistValueExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistValueExpr" ):
                return visitor.visitExistValueExpr(self)
            else:
                return visitor.visitChildren(self)




    def existValueExpr(self):

        localctx = XQueryParser.ExistValueExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 158, self.RULE_existValueExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1138
            self.match(XQueryParser.KW_VALUE)
            self.state = 1139
            self.expr()
            self.state = 1140
            self.match(XQueryParser.KW_WITH)
            self.state = 1141
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistInsertExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_INSERT(self):
            return self.getToken(XQueryParser.KW_INSERT, 0)

        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def KW_INTO(self):
            return self.getToken(XQueryParser.KW_INTO, 0)

        def KW_PRECEDING(self):
            return self.getToken(XQueryParser.KW_PRECEDING, 0)

        def KW_FOLLOWING(self):
            return self.getToken(XQueryParser.KW_FOLLOWING, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_existInsertExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistInsertExpr" ):
                listener.enterExistInsertExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistInsertExpr" ):
                listener.exitExistInsertExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistInsertExpr" ):
                return visitor.visitExistInsertExpr(self)
            else:
                return visitor.visitChildren(self)




    def existInsertExpr(self):

        localctx = XQueryParser.ExistInsertExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 160, self.RULE_existInsertExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1143
            self.match(XQueryParser.KW_INSERT)
            self.state = 1144
            self.exprSingle()
            self.state = 1145
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_FOLLOWING or _la==XQueryParser.KW_PRECEDING or _la==XQueryParser.KW_INTO):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1146
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistDeleteExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DELETE(self):
            return self.getToken(XQueryParser.KW_DELETE, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_existDeleteExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistDeleteExpr" ):
                listener.enterExistDeleteExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistDeleteExpr" ):
                listener.exitExistDeleteExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistDeleteExpr" ):
                return visitor.visitExistDeleteExpr(self)
            else:
                return visitor.visitChildren(self)




    def existDeleteExpr(self):

        localctx = XQueryParser.ExistDeleteExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 162, self.RULE_existDeleteExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1148
            self.match(XQueryParser.KW_DELETE)
            self.state = 1149
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExistRenameExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_RENAME(self):
            return self.getToken(XQueryParser.KW_RENAME, 0)

        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_existRenameExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExistRenameExpr" ):
                listener.enterExistRenameExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExistRenameExpr" ):
                listener.exitExistRenameExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExistRenameExpr" ):
                return visitor.visitExistRenameExpr(self)
            else:
                return visitor.visitChildren(self)




    def existRenameExpr(self):

        localctx = XQueryParser.ExistRenameExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 164, self.RULE_existRenameExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1151
            self.match(XQueryParser.KW_RENAME)
            self.state = 1152
            self.exprSingle()
            self.state = 1153
            self.match(XQueryParser.KW_AS)
            self.state = 1154
            self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.AndExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.AndExprContext,i)


        def KW_OR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_OR)
            else:
                return self.getToken(XQueryParser.KW_OR, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_orExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def orExpr(self):

        localctx = XQueryParser.OrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 166, self.RULE_orExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1156
            self.andExpr()
            self.state = 1161
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,81,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1157
                    self.match(XQueryParser.KW_OR)
                    self.state = 1158
                    self.andExpr() 
                self.state = 1163
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,81,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparisonExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ComparisonExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ComparisonExprContext,i)


        def KW_AND(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_AND)
            else:
                return self.getToken(XQueryParser.KW_AND, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_andExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def andExpr(self):

        localctx = XQueryParser.AndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 168, self.RULE_andExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1164
            self.comparisonExpr()
            self.state = 1169
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,82,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1165
                    self.match(XQueryParser.KW_AND)
                    self.state = 1166
                    self.comparisonExpr() 
                self.state = 1171
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,82,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringConcatExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringConcatExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringConcatExprContext,i)


        def valueComp(self):
            return self.getTypedRuleContext(XQueryParser.ValueCompContext,0)


        def generalComp(self):
            return self.getTypedRuleContext(XQueryParser.GeneralCompContext,0)


        def nodeComp(self):
            return self.getTypedRuleContext(XQueryParser.NodeCompContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_comparisonExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpr" ):
                listener.enterComparisonExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpr" ):
                listener.exitComparisonExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpr" ):
                return visitor.visitComparisonExpr(self)
            else:
                return visitor.visitChildren(self)




    def comparisonExpr(self):

        localctx = XQueryParser.ComparisonExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 170, self.RULE_comparisonExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1172
            self.stringConcatExpr()
            self.state = 1180
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,84,self._ctx)
            if la_ == 1:
                self.state = 1176
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,83,self._ctx)
                if la_ == 1:
                    self.state = 1173
                    self.valueComp()
                    pass

                elif la_ == 2:
                    self.state = 1174
                    self.generalComp()
                    pass

                elif la_ == 3:
                    self.state = 1175
                    self.nodeComp()
                    pass


                self.state = 1178
                self.stringConcatExpr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringConcatExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rangeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.RangeExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.RangeExprContext,i)


        def CONCATENATION(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.CONCATENATION)
            else:
                return self.getToken(XQueryParser.CONCATENATION, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_stringConcatExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringConcatExpr" ):
                listener.enterStringConcatExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringConcatExpr" ):
                listener.exitStringConcatExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringConcatExpr" ):
                return visitor.visitStringConcatExpr(self)
            else:
                return visitor.visitChildren(self)




    def stringConcatExpr(self):

        localctx = XQueryParser.StringConcatExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 172, self.RULE_stringConcatExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1182
            self.rangeExpr()
            self.state = 1187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.CONCATENATION:
                self.state = 1183
                self.match(XQueryParser.CONCATENATION)
                self.state = 1184
                self.rangeExpr()
                self.state = 1189
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RangeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.AdditiveExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.AdditiveExprContext,i)


        def KW_TO(self):
            return self.getToken(XQueryParser.KW_TO, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_rangeExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRangeExpr" ):
                listener.enterRangeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRangeExpr" ):
                listener.exitRangeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRangeExpr" ):
                return visitor.visitRangeExpr(self)
            else:
                return visitor.visitChildren(self)




    def rangeExpr(self):

        localctx = XQueryParser.RangeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 174, self.RULE_rangeExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1190
            self.additiveExpr()
            self.state = 1193
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,86,self._ctx)
            if la_ == 1:
                self.state = 1191
                self.match(XQueryParser.KW_TO)
                self.state = 1192
                self.additiveExpr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.MultiplicativeExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.MultiplicativeExprContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PLUS)
            else:
                return self.getToken(XQueryParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.MINUS)
            else:
                return self.getToken(XQueryParser.MINUS, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_additiveExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpr" ):
                listener.enterAdditiveExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpr" ):
                listener.exitAdditiveExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpr(self):

        localctx = XQueryParser.AdditiveExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 176, self.RULE_additiveExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1195
            self.multiplicativeExpr()
            self.state = 1200
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,87,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1196
                    _la = self._input.LA(1)
                    if not(_la==XQueryParser.PLUS or _la==XQueryParser.MINUS):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 1197
                    self.multiplicativeExpr() 
                self.state = 1202
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,87,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unionExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.UnionExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.UnionExprContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.STAR)
            else:
                return self.getToken(XQueryParser.STAR, i)

        def KW_DIV(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_DIV)
            else:
                return self.getToken(XQueryParser.KW_DIV, i)

        def KW_IDIV(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_IDIV)
            else:
                return self.getToken(XQueryParser.KW_IDIV, i)

        def KW_MOD(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_MOD)
            else:
                return self.getToken(XQueryParser.KW_MOD, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_multiplicativeExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpr" ):
                listener.enterMultiplicativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpr" ):
                listener.exitMultiplicativeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpr(self):

        localctx = XQueryParser.MultiplicativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 178, self.RULE_multiplicativeExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1203
            self.unionExpr()
            self.state = 1208
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,88,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1204
                    _la = self._input.LA(1)
                    if not(_la==XQueryParser.STAR or ((((_la - 83)) & ~0x3f) == 0 and ((1 << (_la - 83)) & ((1 << (XQueryParser.KW_DIV - 83)) | (1 << (XQueryParser.KW_IDIV - 83)) | (1 << (XQueryParser.KW_MOD - 83)))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 1205
                    self.unionExpr() 
                self.state = 1210
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,88,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnionExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def intersectExceptExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.IntersectExceptExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.IntersectExceptExprContext,i)


        def KW_UNION(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_UNION)
            else:
                return self.getToken(XQueryParser.KW_UNION, i)

        def VBAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.VBAR)
            else:
                return self.getToken(XQueryParser.VBAR, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_unionExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnionExpr" ):
                listener.enterUnionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnionExpr" ):
                listener.exitUnionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnionExpr" ):
                return visitor.visitUnionExpr(self)
            else:
                return visitor.visitChildren(self)




    def unionExpr(self):

        localctx = XQueryParser.UnionExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 180, self.RULE_unionExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1211
            self.intersectExceptExpr()
            self.state = 1216
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,89,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1212
                    _la = self._input.LA(1)
                    if not(_la==XQueryParser.VBAR or _la==XQueryParser.KW_UNION):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 1213
                    self.intersectExceptExpr() 
                self.state = 1218
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,89,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntersectExceptExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def instanceOfExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.InstanceOfExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.InstanceOfExprContext,i)


        def KW_INTERSECT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_INTERSECT)
            else:
                return self.getToken(XQueryParser.KW_INTERSECT, i)

        def KW_EXCEPT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_EXCEPT)
            else:
                return self.getToken(XQueryParser.KW_EXCEPT, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_intersectExceptExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntersectExceptExpr" ):
                listener.enterIntersectExceptExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntersectExceptExpr" ):
                listener.exitIntersectExceptExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntersectExceptExpr" ):
                return visitor.visitIntersectExceptExpr(self)
            else:
                return visitor.visitChildren(self)




    def intersectExceptExpr(self):

        localctx = XQueryParser.IntersectExceptExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 182, self.RULE_intersectExceptExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1219
            self.instanceOfExpr()
            self.state = 1224
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,90,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1220
                    _la = self._input.LA(1)
                    if not(_la==XQueryParser.KW_EXCEPT or _la==XQueryParser.KW_INTERSECT):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 1221
                    self.instanceOfExpr() 
                self.state = 1226
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,90,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstanceOfExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def treatExpr(self):
            return self.getTypedRuleContext(XQueryParser.TreatExprContext,0)


        def KW_INSTANCE(self):
            return self.getToken(XQueryParser.KW_INSTANCE, 0)

        def KW_OF(self):
            return self.getToken(XQueryParser.KW_OF, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_instanceOfExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInstanceOfExpr" ):
                listener.enterInstanceOfExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInstanceOfExpr" ):
                listener.exitInstanceOfExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstanceOfExpr" ):
                return visitor.visitInstanceOfExpr(self)
            else:
                return visitor.visitChildren(self)




    def instanceOfExpr(self):

        localctx = XQueryParser.InstanceOfExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 184, self.RULE_instanceOfExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1227
            self.treatExpr()
            self.state = 1231
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,91,self._ctx)
            if la_ == 1:
                self.state = 1228
                self.match(XQueryParser.KW_INSTANCE)
                self.state = 1229
                self.match(XQueryParser.KW_OF)
                self.state = 1230
                self.sequenceType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TreatExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def castableExpr(self):
            return self.getTypedRuleContext(XQueryParser.CastableExprContext,0)


        def KW_TREAT(self):
            return self.getToken(XQueryParser.KW_TREAT, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_treatExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTreatExpr" ):
                listener.enterTreatExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTreatExpr" ):
                listener.exitTreatExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTreatExpr" ):
                return visitor.visitTreatExpr(self)
            else:
                return visitor.visitChildren(self)




    def treatExpr(self):

        localctx = XQueryParser.TreatExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 186, self.RULE_treatExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1233
            self.castableExpr()
            self.state = 1237
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,92,self._ctx)
            if la_ == 1:
                self.state = 1234
                self.match(XQueryParser.KW_TREAT)
                self.state = 1235
                self.match(XQueryParser.KW_AS)
                self.state = 1236
                self.sequenceType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CastableExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def castExpr(self):
            return self.getTypedRuleContext(XQueryParser.CastExprContext,0)


        def KW_CASTABLE(self):
            return self.getToken(XQueryParser.KW_CASTABLE, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def singleType(self):
            return self.getTypedRuleContext(XQueryParser.SingleTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_castableExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCastableExpr" ):
                listener.enterCastableExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCastableExpr" ):
                listener.exitCastableExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCastableExpr" ):
                return visitor.visitCastableExpr(self)
            else:
                return visitor.visitChildren(self)




    def castableExpr(self):

        localctx = XQueryParser.CastableExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 188, self.RULE_castableExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1239
            self.castExpr()
            self.state = 1243
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,93,self._ctx)
            if la_ == 1:
                self.state = 1240
                self.match(XQueryParser.KW_CASTABLE)
                self.state = 1241
                self.match(XQueryParser.KW_AS)
                self.state = 1242
                self.singleType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CastExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arrowExpr(self):
            return self.getTypedRuleContext(XQueryParser.ArrowExprContext,0)


        def KW_CAST(self):
            return self.getToken(XQueryParser.KW_CAST, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def singleType(self):
            return self.getTypedRuleContext(XQueryParser.SingleTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_castExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCastExpr" ):
                listener.enterCastExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCastExpr" ):
                listener.exitCastExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCastExpr" ):
                return visitor.visitCastExpr(self)
            else:
                return visitor.visitChildren(self)




    def castExpr(self):

        localctx = XQueryParser.CastExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 190, self.RULE_castExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1245
            self.arrowExpr()
            self.state = 1249
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,94,self._ctx)
            if la_ == 1:
                self.state = 1246
                self.match(XQueryParser.KW_CAST)
                self.state = 1247
                self.match(XQueryParser.KW_AS)
                self.state = 1248
                self.singleType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrowExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpression(self):
            return self.getTypedRuleContext(XQueryParser.UnaryExpressionContext,0)


        def ARROW(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ARROW)
            else:
                return self.getToken(XQueryParser.ARROW, i)

        def arrowFunctionSpecifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ArrowFunctionSpecifierContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ArrowFunctionSpecifierContext,i)


        def argumentList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ArgumentListContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ArgumentListContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_arrowExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrowExpr" ):
                listener.enterArrowExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrowExpr" ):
                listener.exitArrowExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrowExpr" ):
                return visitor.visitArrowExpr(self)
            else:
                return visitor.visitChildren(self)




    def arrowExpr(self):

        localctx = XQueryParser.ArrowExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 192, self.RULE_arrowExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1251
            self.unaryExpression()
            self.state = 1258
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,95,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1252
                    self.match(XQueryParser.ARROW)
                    self.state = 1253
                    self.arrowFunctionSpecifier()
                    self.state = 1254
                    self.argumentList() 
                self.state = 1260
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,95,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def valueExpr(self):
            return self.getTypedRuleContext(XQueryParser.ValueExprContext,0)


        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.MINUS)
            else:
                return self.getToken(XQueryParser.MINUS, i)

        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PLUS)
            else:
                return self.getToken(XQueryParser.PLUS, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_unaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpression" ):
                listener.enterUnaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpression" ):
                listener.exitUnaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpression" ):
                return visitor.visitUnaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpression(self):

        localctx = XQueryParser.UnaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 194, self.RULE_unaryExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1264
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.PLUS or _la==XQueryParser.MINUS:
                self.state = 1261
                _la = self._input.LA(1)
                if not(_la==XQueryParser.PLUS or _la==XQueryParser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 1266
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1267
            self.valueExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def validateExpr(self):
            return self.getTypedRuleContext(XQueryParser.ValidateExprContext,0)


        def extensionExpr(self):
            return self.getTypedRuleContext(XQueryParser.ExtensionExprContext,0)


        def simpleMapExpr(self):
            return self.getTypedRuleContext(XQueryParser.SimpleMapExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_valueExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValueExpr" ):
                listener.enterValueExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValueExpr" ):
                listener.exitValueExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueExpr" ):
                return visitor.visitValueExpr(self)
            else:
                return visitor.visitChildren(self)




    def valueExpr(self):

        localctx = XQueryParser.ValueExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 196, self.RULE_valueExpr)
        try:
            self.state = 1272
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,97,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1269
                self.validateExpr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1270
                self.extensionExpr()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1271
                self.simpleMapExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GeneralCompContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQUAL(self):
            return self.getToken(XQueryParser.EQUAL, 0)

        def NOT_EQUAL(self):
            return self.getToken(XQueryParser.NOT_EQUAL, 0)

        def LANGLE(self):
            return self.getToken(XQueryParser.LANGLE, 0)

        def RANGLE(self):
            return self.getToken(XQueryParser.RANGLE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_generalComp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeneralComp" ):
                listener.enterGeneralComp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeneralComp" ):
                listener.exitGeneralComp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneralComp" ):
                return visitor.visitGeneralComp(self)
            else:
                return visitor.visitChildren(self)




    def generalComp(self):

        localctx = XQueryParser.GeneralCompContext(self, self._ctx, self.state)
        self.enterRule(localctx, 198, self.RULE_generalComp)
        try:
            self.state = 1282
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,98,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1274
                self.match(XQueryParser.EQUAL)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1275
                self.match(XQueryParser.NOT_EQUAL)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1276
                self.match(XQueryParser.LANGLE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1277
                self.match(XQueryParser.LANGLE)
                self.state = 1278
                self.match(XQueryParser.EQUAL)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1279
                self.match(XQueryParser.RANGLE)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1280
                self.match(XQueryParser.RANGLE)
                self.state = 1281
                self.match(XQueryParser.EQUAL)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueCompContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_EQ(self):
            return self.getToken(XQueryParser.KW_EQ, 0)

        def KW_NE(self):
            return self.getToken(XQueryParser.KW_NE, 0)

        def KW_LT(self):
            return self.getToken(XQueryParser.KW_LT, 0)

        def KW_LE(self):
            return self.getToken(XQueryParser.KW_LE, 0)

        def KW_GT(self):
            return self.getToken(XQueryParser.KW_GT, 0)

        def KW_GE(self):
            return self.getToken(XQueryParser.KW_GE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_valueComp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValueComp" ):
                listener.enterValueComp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValueComp" ):
                listener.exitValueComp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueComp" ):
                return visitor.visitValueComp(self)
            else:
                return visitor.visitChildren(self)




    def valueComp(self):

        localctx = XQueryParser.ValueCompContext(self, self._ctx, self.state)
        self.enterRule(localctx, 200, self.RULE_valueComp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1284
            _la = self._input.LA(1)
            if not(((((_la - 92)) & ~0x3f) == 0 and ((1 << (_la - 92)) & ((1 << (XQueryParser.KW_EQ - 92)) | (1 << (XQueryParser.KW_GE - 92)) | (1 << (XQueryParser.KW_GT - 92)) | (1 << (XQueryParser.KW_LE - 92)) | (1 << (XQueryParser.KW_LT - 92)) | (1 << (XQueryParser.KW_NE - 92)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeCompContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_IS(self):
            return self.getToken(XQueryParser.KW_IS, 0)

        def LANGLE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.LANGLE)
            else:
                return self.getToken(XQueryParser.LANGLE, i)

        def RANGLE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.RANGLE)
            else:
                return self.getToken(XQueryParser.RANGLE, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_nodeComp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeComp" ):
                listener.enterNodeComp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeComp" ):
                listener.exitNodeComp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNodeComp" ):
                return visitor.visitNodeComp(self)
            else:
                return visitor.visitChildren(self)




    def nodeComp(self):

        localctx = XQueryParser.NodeCompContext(self, self._ctx, self.state)
        self.enterRule(localctx, 202, self.RULE_nodeComp)
        try:
            self.state = 1291
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_IS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1286
                self.match(XQueryParser.KW_IS)
                pass
            elif token in [XQueryParser.LANGLE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1287
                self.match(XQueryParser.LANGLE)
                self.state = 1288
                self.match(XQueryParser.LANGLE)
                pass
            elif token in [XQueryParser.RANGLE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1289
                self.match(XQueryParser.RANGLE)
                self.state = 1290
                self.match(XQueryParser.RANGLE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValidateExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_VALIDATE(self):
            return self.getToken(XQueryParser.KW_VALIDATE, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def validationMode(self):
            return self.getTypedRuleContext(XQueryParser.ValidationModeContext,0)


        def typeName(self):
            return self.getTypedRuleContext(XQueryParser.TypeNameContext,0)


        def KW_TYPE(self):
            return self.getToken(XQueryParser.KW_TYPE, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_validateExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValidateExpr" ):
                listener.enterValidateExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValidateExpr" ):
                listener.exitValidateExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValidateExpr" ):
                return visitor.visitValidateExpr(self)
            else:
                return visitor.visitChildren(self)




    def validateExpr(self):

        localctx = XQueryParser.ValidateExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 204, self.RULE_validateExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1293
            self.match(XQueryParser.KW_VALIDATE)
            self.state = 1297
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_LAX, XQueryParser.KW_STRICT]:
                self.state = 1294
                self.validationMode()
                pass
            elif token in [XQueryParser.KW_AS, XQueryParser.KW_TYPE]:
                self.state = 1295
                _la = self._input.LA(1)
                if not(_la==XQueryParser.KW_AS or _la==XQueryParser.KW_TYPE):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 1296
                self.typeName()
                pass
            elif token in [XQueryParser.LBRACE]:
                pass
            else:
                pass
            self.state = 1299
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValidationModeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_LAX(self):
            return self.getToken(XQueryParser.KW_LAX, 0)

        def KW_STRICT(self):
            return self.getToken(XQueryParser.KW_STRICT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_validationMode

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValidationMode" ):
                listener.enterValidationMode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValidationMode" ):
                listener.exitValidationMode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValidationMode" ):
                return visitor.visitValidationMode(self)
            else:
                return visitor.visitChildren(self)




    def validationMode(self):

        localctx = XQueryParser.ValidationModeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 206, self.RULE_validationMode)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1301
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_LAX or _la==XQueryParser.KW_STRICT):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExtensionExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def PRAGMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PRAGMA)
            else:
                return self.getToken(XQueryParser.PRAGMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_extensionExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExtensionExpr" ):
                listener.enterExtensionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExtensionExpr" ):
                listener.exitExtensionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtensionExpr" ):
                return visitor.visitExtensionExpr(self)
            else:
                return visitor.visitChildren(self)




    def extensionExpr(self):

        localctx = XQueryParser.ExtensionExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 208, self.RULE_extensionExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1304 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 1303
                self.match(XQueryParser.PRAGMA)
                self.state = 1306 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==XQueryParser.PRAGMA):
                    break

            self.state = 1308
            self.match(XQueryParser.LBRACE)
            self.state = 1309
            self.expr()
            self.state = 1310
            self.match(XQueryParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleMapExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pathExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.PathExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.PathExprContext,i)


        def BANG(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.BANG)
            else:
                return self.getToken(XQueryParser.BANG, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_simpleMapExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleMapExpr" ):
                listener.enterSimpleMapExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleMapExpr" ):
                listener.exitSimpleMapExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleMapExpr" ):
                return visitor.visitSimpleMapExpr(self)
            else:
                return visitor.visitChildren(self)




    def simpleMapExpr(self):

        localctx = XQueryParser.SimpleMapExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 210, self.RULE_simpleMapExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1312
            self.pathExpr()
            self.state = 1317
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,102,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1313
                    self.match(XQueryParser.BANG)
                    self.state = 1314
                    self.pathExpr() 
                self.state = 1319
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,102,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLASH(self):
            return self.getToken(XQueryParser.SLASH, 0)

        def relativePathExpr(self):
            return self.getTypedRuleContext(XQueryParser.RelativePathExprContext,0)


        def DSLASH(self):
            return self.getToken(XQueryParser.DSLASH, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_pathExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathExpr" ):
                listener.enterPathExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathExpr" ):
                listener.exitPathExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathExpr" ):
                return visitor.visitPathExpr(self)
            else:
                return visitor.visitChildren(self)




    def pathExpr(self):

        localctx = XQueryParser.PathExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 212, self.RULE_pathExpr)
        try:
            self.state = 1327
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.SLASH]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1320
                self.match(XQueryParser.SLASH)
                self.state = 1322
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,103,self._ctx)
                if la_ == 1:
                    self.state = 1321
                    self.relativePathExpr()


                pass
            elif token in [XQueryParser.DSLASH]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1324
                self.match(XQueryParser.DSLASH)
                self.state = 1325
                self.relativePathExpr()
                pass
            elif token in [XQueryParser.IntegerLiteral, XQueryParser.DecimalLiteral, XQueryParser.DoubleLiteral, XQueryParser.DFPropertyName, XQueryParser.Quot, XQueryParser.Apos, XQueryParser.COMMENT, XQueryParser.PI, XQueryParser.LPAREN, XQueryParser.LBRACKET, XQueryParser.STAR, XQueryParser.DOT, XQueryParser.DDOT, XQueryParser.LANGLE, XQueryParser.QUESTION, XQueryParser.AT, XQueryParser.DOLLAR, XQueryParser.MOD, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCNameWithLocalWildcard, XQueryParser.NCNameWithPrefixWildcard, XQueryParser.NCName, XQueryParser.ENTER_STRING]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1326
                self.relativePathExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelativePathExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.sep = None # Token

        def stepExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StepExprContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StepExprContext,i)


        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.SLASH)
            else:
                return self.getToken(XQueryParser.SLASH, i)

        def DSLASH(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DSLASH)
            else:
                return self.getToken(XQueryParser.DSLASH, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_relativePathExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelativePathExpr" ):
                listener.enterRelativePathExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelativePathExpr" ):
                listener.exitRelativePathExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelativePathExpr" ):
                return visitor.visitRelativePathExpr(self)
            else:
                return visitor.visitChildren(self)




    def relativePathExpr(self):

        localctx = XQueryParser.RelativePathExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 214, self.RULE_relativePathExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1329
            self.stepExpr()
            self.state = 1334
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,105,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1330
                    localctx.sep = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==XQueryParser.SLASH or _la==XQueryParser.DSLASH):
                        localctx.sep = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 1331
                    self.stepExpr() 
                self.state = 1336
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,105,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StepExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def postfixExpr(self):
            return self.getTypedRuleContext(XQueryParser.PostfixExprContext,0)


        def axisStep(self):
            return self.getTypedRuleContext(XQueryParser.AxisStepContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_stepExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStepExpr" ):
                listener.enterStepExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStepExpr" ):
                listener.exitStepExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStepExpr" ):
                return visitor.visitStepExpr(self)
            else:
                return visitor.visitChildren(self)




    def stepExpr(self):

        localctx = XQueryParser.StepExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 216, self.RULE_stepExpr)
        try:
            self.state = 1339
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,106,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1337
                self.postfixExpr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1338
                self.axisStep()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AxisStepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicateList(self):
            return self.getTypedRuleContext(XQueryParser.PredicateListContext,0)


        def reverseStep(self):
            return self.getTypedRuleContext(XQueryParser.ReverseStepContext,0)


        def forwardStep(self):
            return self.getTypedRuleContext(XQueryParser.ForwardStepContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_axisStep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAxisStep" ):
                listener.enterAxisStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAxisStep" ):
                listener.exitAxisStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAxisStep" ):
                return visitor.visitAxisStep(self)
            else:
                return visitor.visitChildren(self)




    def axisStep(self):

        localctx = XQueryParser.AxisStepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 218, self.RULE_axisStep)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1343
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,107,self._ctx)
            if la_ == 1:
                self.state = 1341
                self.reverseStep()
                pass

            elif la_ == 2:
                self.state = 1342
                self.forwardStep()
                pass


            self.state = 1345
            self.predicateList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForwardStepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def forwardAxis(self):
            return self.getTypedRuleContext(XQueryParser.ForwardAxisContext,0)


        def nodeTest(self):
            return self.getTypedRuleContext(XQueryParser.NodeTestContext,0)


        def abbrevForwardStep(self):
            return self.getTypedRuleContext(XQueryParser.AbbrevForwardStepContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_forwardStep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForwardStep" ):
                listener.enterForwardStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForwardStep" ):
                listener.exitForwardStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForwardStep" ):
                return visitor.visitForwardStep(self)
            else:
                return visitor.visitChildren(self)




    def forwardStep(self):

        localctx = XQueryParser.ForwardStepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 220, self.RULE_forwardStep)
        try:
            self.state = 1351
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,108,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1347
                self.forwardAxis()
                self.state = 1348
                self.nodeTest()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1350
                self.abbrevForwardStep()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForwardAxisContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COLON)
            else:
                return self.getToken(XQueryParser.COLON, i)

        def KW_CHILD(self):
            return self.getToken(XQueryParser.KW_CHILD, 0)

        def KW_DESCENDANT(self):
            return self.getToken(XQueryParser.KW_DESCENDANT, 0)

        def KW_ATTRIBUTE(self):
            return self.getToken(XQueryParser.KW_ATTRIBUTE, 0)

        def KW_SELF(self):
            return self.getToken(XQueryParser.KW_SELF, 0)

        def KW_DESCENDANT_OR_SELF(self):
            return self.getToken(XQueryParser.KW_DESCENDANT_OR_SELF, 0)

        def KW_FOLLOWING_SIBLING(self):
            return self.getToken(XQueryParser.KW_FOLLOWING_SIBLING, 0)

        def KW_FOLLOWING(self):
            return self.getToken(XQueryParser.KW_FOLLOWING, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_forwardAxis

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForwardAxis" ):
                listener.enterForwardAxis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForwardAxis" ):
                listener.exitForwardAxis(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForwardAxis" ):
                return visitor.visitForwardAxis(self)
            else:
                return visitor.visitChildren(self)




    def forwardAxis(self):

        localctx = XQueryParser.ForwardAxisContext(self, self._ctx, self.state)
        self.enterRule(localctx, 222, self.RULE_forwardAxis)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1353
            _la = self._input.LA(1)
            if not(((((_la - 61)) & ~0x3f) == 0 and ((1 << (_la - 61)) & ((1 << (XQueryParser.KW_ATTRIBUTE - 61)) | (1 << (XQueryParser.KW_CHILD - 61)) | (1 << (XQueryParser.KW_DESCENDANT - 61)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 61)) | (1 << (XQueryParser.KW_FOLLOWING - 61)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 61)))) != 0) or _la==XQueryParser.KW_SELF):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1354
            self.match(XQueryParser.COLON)
            self.state = 1355
            self.match(XQueryParser.COLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AbbrevForwardStepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def nodeTest(self):
            return self.getTypedRuleContext(XQueryParser.NodeTestContext,0)


        def AT(self):
            return self.getToken(XQueryParser.AT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_abbrevForwardStep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbbrevForwardStep" ):
                listener.enterAbbrevForwardStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbbrevForwardStep" ):
                listener.exitAbbrevForwardStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbbrevForwardStep" ):
                return visitor.visitAbbrevForwardStep(self)
            else:
                return visitor.visitChildren(self)




    def abbrevForwardStep(self):

        localctx = XQueryParser.AbbrevForwardStepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 224, self.RULE_abbrevForwardStep)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1358
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.AT:
                self.state = 1357
                self.match(XQueryParser.AT)


            self.state = 1360
            self.nodeTest()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReverseStepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def reverseAxis(self):
            return self.getTypedRuleContext(XQueryParser.ReverseAxisContext,0)


        def nodeTest(self):
            return self.getTypedRuleContext(XQueryParser.NodeTestContext,0)


        def abbrevReverseStep(self):
            return self.getTypedRuleContext(XQueryParser.AbbrevReverseStepContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_reverseStep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReverseStep" ):
                listener.enterReverseStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReverseStep" ):
                listener.exitReverseStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReverseStep" ):
                return visitor.visitReverseStep(self)
            else:
                return visitor.visitChildren(self)




    def reverseStep(self):

        localctx = XQueryParser.ReverseStepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 226, self.RULE_reverseStep)
        try:
            self.state = 1366
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1362
                self.reverseAxis()
                self.state = 1363
                self.nodeTest()
                pass
            elif token in [XQueryParser.DDOT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1365
                self.abbrevReverseStep()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReverseAxisContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COLON)
            else:
                return self.getToken(XQueryParser.COLON, i)

        def KW_PARENT(self):
            return self.getToken(XQueryParser.KW_PARENT, 0)

        def KW_ANCESTOR(self):
            return self.getToken(XQueryParser.KW_ANCESTOR, 0)

        def KW_PRECEDING_SIBLING(self):
            return self.getToken(XQueryParser.KW_PRECEDING_SIBLING, 0)

        def KW_PRECEDING(self):
            return self.getToken(XQueryParser.KW_PRECEDING, 0)

        def KW_ANCESTOR_OR_SELF(self):
            return self.getToken(XQueryParser.KW_ANCESTOR_OR_SELF, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_reverseAxis

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReverseAxis" ):
                listener.enterReverseAxis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReverseAxis" ):
                listener.exitReverseAxis(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReverseAxis" ):
                return visitor.visitReverseAxis(self)
            else:
                return visitor.visitChildren(self)




    def reverseAxis(self):

        localctx = XQueryParser.ReverseAxisContext(self, self._ctx, self.state)
        self.enterRule(localctx, 228, self.RULE_reverseAxis)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1368
            _la = self._input.LA(1)
            if not(_la==XQueryParser.KW_ANCESTOR or _la==XQueryParser.KW_ANCESTOR_OR_SELF or ((((_la - 135)) & ~0x3f) == 0 and ((1 << (_la - 135)) & ((1 << (XQueryParser.KW_PARENT - 135)) | (1 << (XQueryParser.KW_PRECEDING - 135)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 135)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1369
            self.match(XQueryParser.COLON)
            self.state = 1370
            self.match(XQueryParser.COLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AbbrevReverseStepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DDOT(self):
            return self.getToken(XQueryParser.DDOT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_abbrevReverseStep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbbrevReverseStep" ):
                listener.enterAbbrevReverseStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbbrevReverseStep" ):
                listener.exitAbbrevReverseStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbbrevReverseStep" ):
                return visitor.visitAbbrevReverseStep(self)
            else:
                return visitor.visitChildren(self)




    def abbrevReverseStep(self):

        localctx = XQueryParser.AbbrevReverseStepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 230, self.RULE_abbrevReverseStep)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1372
            self.match(XQueryParser.DDOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def nameTest(self):
            return self.getTypedRuleContext(XQueryParser.NameTestContext,0)


        def kindTest(self):
            return self.getTypedRuleContext(XQueryParser.KindTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_nodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeTest" ):
                listener.enterNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeTest" ):
                listener.exitNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNodeTest" ):
                return visitor.visitNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def nodeTest(self):

        localctx = XQueryParser.NodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 232, self.RULE_nodeTest)
        try:
            self.state = 1376
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,111,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1374
                self.nameTest()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1375
                self.kindTest()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def wildcard(self):
            return self.getTypedRuleContext(XQueryParser.WildcardContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_nameTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNameTest" ):
                listener.enterNameTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNameTest" ):
                listener.exitNameTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNameTest" ):
                return visitor.visitNameTest(self)
            else:
                return visitor.visitChildren(self)




    def nameTest(self):

        localctx = XQueryParser.NameTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 234, self.RULE_nameTest)
        try:
            self.state = 1380
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1378
                self.eqName()
                pass
            elif token in [XQueryParser.STAR, XQueryParser.NCNameWithLocalWildcard, XQueryParser.NCNameWithPrefixWildcard]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1379
                self.wildcard()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WildcardContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return XQueryParser.RULE_wildcard

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AllNamesContext(WildcardContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a XQueryParser.WildcardContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAllNames" ):
                listener.enterAllNames(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAllNames" ):
                listener.exitAllNames(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAllNames" ):
                return visitor.visitAllNames(self)
            else:
                return visitor.visitChildren(self)


    class AllWithLocalContext(WildcardContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a XQueryParser.WildcardContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NCNameWithPrefixWildcard(self):
            return self.getToken(XQueryParser.NCNameWithPrefixWildcard, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAllWithLocal" ):
                listener.enterAllWithLocal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAllWithLocal" ):
                listener.exitAllWithLocal(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAllWithLocal" ):
                return visitor.visitAllWithLocal(self)
            else:
                return visitor.visitChildren(self)


    class AllWithNSContext(WildcardContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a XQueryParser.WildcardContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NCNameWithLocalWildcard(self):
            return self.getToken(XQueryParser.NCNameWithLocalWildcard, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAllWithNS" ):
                listener.enterAllWithNS(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAllWithNS" ):
                listener.exitAllWithNS(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAllWithNS" ):
                return visitor.visitAllWithNS(self)
            else:
                return visitor.visitChildren(self)



    def wildcard(self):

        localctx = XQueryParser.WildcardContext(self, self._ctx, self.state)
        self.enterRule(localctx, 236, self.RULE_wildcard)
        try:
            self.state = 1385
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.STAR]:
                localctx = XQueryParser.AllNamesContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 1382
                self.match(XQueryParser.STAR)
                pass
            elif token in [XQueryParser.NCNameWithLocalWildcard]:
                localctx = XQueryParser.AllWithNSContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 1383
                self.match(XQueryParser.NCNameWithLocalWildcard)
                pass
            elif token in [XQueryParser.NCNameWithPrefixWildcard]:
                localctx = XQueryParser.AllWithLocalContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 1384
                self.match(XQueryParser.NCNameWithPrefixWildcard)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primaryExpr(self):
            return self.getTypedRuleContext(XQueryParser.PrimaryExprContext,0)


        def predicate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.PredicateContext)
            else:
                return self.getTypedRuleContext(XQueryParser.PredicateContext,i)


        def argumentList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ArgumentListContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ArgumentListContext,i)


        def lookup(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.LookupContext)
            else:
                return self.getTypedRuleContext(XQueryParser.LookupContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_postfixExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixExpr" ):
                listener.enterPostfixExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixExpr" ):
                listener.exitPostfixExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixExpr" ):
                return visitor.visitPostfixExpr(self)
            else:
                return visitor.visitChildren(self)




    def postfixExpr(self):

        localctx = XQueryParser.PostfixExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 238, self.RULE_postfixExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1387
            self.primaryExpr()
            self.state = 1393
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,115,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1391
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [XQueryParser.LBRACKET]:
                        self.state = 1388
                        self.predicate()
                        pass
                    elif token in [XQueryParser.LPAREN]:
                        self.state = 1389
                        self.argumentList()
                        pass
                    elif token in [XQueryParser.QUESTION]:
                        self.state = 1390
                        self.lookup()
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 1395
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,115,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ArgumentContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_argumentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgumentList" ):
                listener.enterArgumentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgumentList" ):
                listener.exitArgumentList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgumentList" ):
                return visitor.visitArgumentList(self)
            else:
                return visitor.visitChildren(self)




    def argumentList(self):

        localctx = XQueryParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 240, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1396
            self.match(XQueryParser.LPAREN)
            self.state = 1405
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                self.state = 1397
                self.argument()
                self.state = 1402
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 1398
                    self.match(XQueryParser.COMMA)
                    self.state = 1399
                    self.argument()
                    self.state = 1404
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 1407
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.PredicateContext)
            else:
                return self.getTypedRuleContext(XQueryParser.PredicateContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_predicateList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicateList" ):
                listener.enterPredicateList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicateList" ):
                listener.exitPredicateList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicateList" ):
                return visitor.visitPredicateList(self)
            else:
                return visitor.visitChildren(self)




    def predicateList(self):

        localctx = XQueryParser.PredicateListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 242, self.RULE_predicateList)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1412
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,118,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1409
                    self.predicate() 
                self.state = 1414
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,118,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(XQueryParser.LBRACKET, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACKET(self):
            return self.getToken(XQueryParser.RBRACKET, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_predicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate" ):
                listener.enterPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate" ):
                listener.exitPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicate" ):
                return visitor.visitPredicate(self)
            else:
                return visitor.visitChildren(self)




    def predicate(self):

        localctx = XQueryParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 244, self.RULE_predicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1415
            self.match(XQueryParser.LBRACKET)
            self.state = 1416
            self.expr()
            self.state = 1417
            self.match(XQueryParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LookupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUESTION(self):
            return self.getToken(XQueryParser.QUESTION, 0)

        def keySpecifier(self):
            return self.getTypedRuleContext(XQueryParser.KeySpecifierContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_lookup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLookup" ):
                listener.enterLookup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLookup" ):
                listener.exitLookup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLookup" ):
                return visitor.visitLookup(self)
            else:
                return visitor.visitChildren(self)




    def lookup(self):

        localctx = XQueryParser.LookupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 246, self.RULE_lookup)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1419
            self.match(XQueryParser.QUESTION)
            self.state = 1420
            self.keySpecifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeySpecifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def IntegerLiteral(self):
            return self.getToken(XQueryParser.IntegerLiteral, 0)

        def parenthesizedExpr(self):
            return self.getTypedRuleContext(XQueryParser.ParenthesizedExprContext,0)


        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_keySpecifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeySpecifier" ):
                listener.enterKeySpecifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeySpecifier" ):
                listener.exitKeySpecifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeySpecifier" ):
                return visitor.visitKeySpecifier(self)
            else:
                return visitor.visitChildren(self)




    def keySpecifier(self):

        localctx = XQueryParser.KeySpecifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 248, self.RULE_keySpecifier)
        try:
            self.state = 1426
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1422
                self.ncName()
                pass
            elif token in [XQueryParser.IntegerLiteral]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1423
                self.match(XQueryParser.IntegerLiteral)
                pass
            elif token in [XQueryParser.LPAREN]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1424
                self.parenthesizedExpr()
                pass
            elif token in [XQueryParser.STAR]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1425
                self.match(XQueryParser.STAR)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrowFunctionSpecifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def varRef(self):
            return self.getTypedRuleContext(XQueryParser.VarRefContext,0)


        def parenthesizedExpr(self):
            return self.getTypedRuleContext(XQueryParser.ParenthesizedExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_arrowFunctionSpecifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrowFunctionSpecifier" ):
                listener.enterArrowFunctionSpecifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrowFunctionSpecifier" ):
                listener.exitArrowFunctionSpecifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrowFunctionSpecifier" ):
                return visitor.visitArrowFunctionSpecifier(self)
            else:
                return visitor.visitChildren(self)




    def arrowFunctionSpecifier(self):

        localctx = XQueryParser.ArrowFunctionSpecifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 250, self.RULE_arrowFunctionSpecifier)
        try:
            self.state = 1431
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1428
                self.eqName()
                pass
            elif token in [XQueryParser.DOLLAR]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1429
                self.varRef()
                pass
            elif token in [XQueryParser.LPAREN]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1430
                self.parenthesizedExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(XQueryParser.LiteralContext,0)


        def varRef(self):
            return self.getTypedRuleContext(XQueryParser.VarRefContext,0)


        def parenthesizedExpr(self):
            return self.getTypedRuleContext(XQueryParser.ParenthesizedExprContext,0)


        def contextItemExpr(self):
            return self.getTypedRuleContext(XQueryParser.ContextItemExprContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(XQueryParser.FunctionCallContext,0)


        def orderedExpr(self):
            return self.getTypedRuleContext(XQueryParser.OrderedExprContext,0)


        def unorderedExpr(self):
            return self.getTypedRuleContext(XQueryParser.UnorderedExprContext,0)


        def nodeConstructor(self):
            return self.getTypedRuleContext(XQueryParser.NodeConstructorContext,0)


        def functionItemExpr(self):
            return self.getTypedRuleContext(XQueryParser.FunctionItemExprContext,0)


        def mapConstructor(self):
            return self.getTypedRuleContext(XQueryParser.MapConstructorContext,0)


        def arrayConstructor(self):
            return self.getTypedRuleContext(XQueryParser.ArrayConstructorContext,0)


        def stringConstructor(self):
            return self.getTypedRuleContext(XQueryParser.StringConstructorContext,0)


        def unaryLookup(self):
            return self.getTypedRuleContext(XQueryParser.UnaryLookupContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_primaryExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpr" ):
                listener.enterPrimaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpr" ):
                listener.exitPrimaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpr" ):
                return visitor.visitPrimaryExpr(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpr(self):

        localctx = XQueryParser.PrimaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 252, self.RULE_primaryExpr)
        try:
            self.state = 1446
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,121,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1433
                self.literal()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1434
                self.varRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1435
                self.parenthesizedExpr()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1436
                self.contextItemExpr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1437
                self.functionCall()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1438
                self.orderedExpr()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1439
                self.unorderedExpr()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 1440
                self.nodeConstructor()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 1441
                self.functionItemExpr()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 1442
                self.mapConstructor()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 1443
                self.arrayConstructor()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 1444
                self.stringConstructor()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 1445
                self.unaryLookup()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def numericLiteral(self):
            return self.getTypedRuleContext(XQueryParser.NumericLiteralContext,0)


        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = XQueryParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 254, self.RULE_literal)
        try:
            self.state = 1450
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.IntegerLiteral, XQueryParser.DecimalLiteral, XQueryParser.DoubleLiteral]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1448
                self.numericLiteral()
                pass
            elif token in [XQueryParser.Quot, XQueryParser.Apos]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1449
                self.stringLiteral()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumericLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IntegerLiteral(self):
            return self.getToken(XQueryParser.IntegerLiteral, 0)

        def DecimalLiteral(self):
            return self.getToken(XQueryParser.DecimalLiteral, 0)

        def DoubleLiteral(self):
            return self.getToken(XQueryParser.DoubleLiteral, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_numericLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumericLiteral" ):
                listener.enterNumericLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumericLiteral" ):
                listener.exitNumericLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumericLiteral" ):
                return visitor.visitNumericLiteral(self)
            else:
                return visitor.visitChildren(self)




    def numericLiteral(self):

        localctx = XQueryParser.NumericLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 256, self.RULE_numericLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1452
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.IntegerLiteral) | (1 << XQueryParser.DecimalLiteral) | (1 << XQueryParser.DoubleLiteral))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(XQueryParser.DOLLAR, 0)

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_varRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarRef" ):
                listener.enterVarRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarRef" ):
                listener.exitVarRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarRef" ):
                return visitor.visitVarRef(self)
            else:
                return visitor.visitChildren(self)




    def varRef(self):

        localctx = XQueryParser.VarRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 258, self.RULE_varRef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1454
            self.match(XQueryParser.DOLLAR)
            self.state = 1455
            self.eqName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_varName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarName" ):
                listener.enterVarName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarName" ):
                listener.exitVarName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarName" ):
                return visitor.visitVarName(self)
            else:
                return visitor.visitChildren(self)




    def varName(self):

        localctx = XQueryParser.VarNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 260, self.RULE_varName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1457
            self.eqName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParenthesizedExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_parenthesizedExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesizedExpr" ):
                listener.enterParenthesizedExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesizedExpr" ):
                listener.exitParenthesizedExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenthesizedExpr" ):
                return visitor.visitParenthesizedExpr(self)
            else:
                return visitor.visitChildren(self)




    def parenthesizedExpr(self):

        localctx = XQueryParser.ParenthesizedExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 262, self.RULE_parenthesizedExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1459
            self.match(XQueryParser.LPAREN)
            self.state = 1461
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                self.state = 1460
                self.expr()


            self.state = 1463
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContextItemExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(XQueryParser.DOT, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_contextItemExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContextItemExpr" ):
                listener.enterContextItemExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContextItemExpr" ):
                listener.exitContextItemExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContextItemExpr" ):
                return visitor.visitContextItemExpr(self)
            else:
                return visitor.visitChildren(self)




    def contextItemExpr(self):

        localctx = XQueryParser.ContextItemExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 264, self.RULE_contextItemExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1465
            self.match(XQueryParser.DOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderedExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ORDERED(self):
            return self.getToken(XQueryParser.KW_ORDERED, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_orderedExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderedExpr" ):
                listener.enterOrderedExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderedExpr" ):
                listener.exitOrderedExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderedExpr" ):
                return visitor.visitOrderedExpr(self)
            else:
                return visitor.visitChildren(self)




    def orderedExpr(self):

        localctx = XQueryParser.OrderedExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 266, self.RULE_orderedExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1467
            self.match(XQueryParser.KW_ORDERED)
            self.state = 1468
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnorderedExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_UNORDERED(self):
            return self.getToken(XQueryParser.KW_UNORDERED, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_unorderedExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnorderedExpr" ):
                listener.enterUnorderedExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnorderedExpr" ):
                listener.exitUnorderedExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnorderedExpr" ):
                return visitor.visitUnorderedExpr(self)
            else:
                return visitor.visitChildren(self)




    def unorderedExpr(self):

        localctx = XQueryParser.UnorderedExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 268, self.RULE_unorderedExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1470
            self.match(XQueryParser.KW_UNORDERED)
            self.state = 1471
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def argumentList(self):
            return self.getTypedRuleContext(XQueryParser.ArgumentListContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = XQueryParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 270, self.RULE_functionCall)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1473
            self.eqName()
            self.state = 1474
            self.argumentList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def QUESTION(self):
            return self.getToken(XQueryParser.QUESTION, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_argument

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgument" ):
                listener.enterArgument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgument" ):
                listener.exitArgument(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgument" ):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = XQueryParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 272, self.RULE_argument)
        try:
            self.state = 1478
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,124,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1476
                self.exprSingle()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1477
                self.match(XQueryParser.QUESTION)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def directConstructor(self):
            return self.getTypedRuleContext(XQueryParser.DirectConstructorContext,0)


        def computedConstructor(self):
            return self.getTypedRuleContext(XQueryParser.ComputedConstructorContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_nodeConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeConstructor" ):
                listener.enterNodeConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeConstructor" ):
                listener.exitNodeConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNodeConstructor" ):
                return visitor.visitNodeConstructor(self)
            else:
                return visitor.visitChildren(self)




    def nodeConstructor(self):

        localctx = XQueryParser.NodeConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 274, self.RULE_nodeConstructor)
        try:
            self.state = 1482
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.COMMENT, XQueryParser.PI, XQueryParser.LANGLE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1480
                self.directConstructor()
                pass
            elif token in [XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BINARY, XQueryParser.KW_COMMENT, XQueryParser.KW_DOCUMENT, XQueryParser.KW_ELEMENT, XQueryParser.KW_NAMESPACE, XQueryParser.KW_PI, XQueryParser.KW_TEXT, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1481
                self.computedConstructor()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirectConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dirElemConstructorOpenClose(self):
            return self.getTypedRuleContext(XQueryParser.DirElemConstructorOpenCloseContext,0)


        def dirElemConstructorSingleTag(self):
            return self.getTypedRuleContext(XQueryParser.DirElemConstructorSingleTagContext,0)


        def COMMENT(self):
            return self.getToken(XQueryParser.COMMENT, 0)

        def PI(self):
            return self.getToken(XQueryParser.PI, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_directConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirectConstructor" ):
                listener.enterDirectConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirectConstructor" ):
                listener.exitDirectConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirectConstructor" ):
                return visitor.visitDirectConstructor(self)
            else:
                return visitor.visitChildren(self)




    def directConstructor(self):

        localctx = XQueryParser.DirectConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 276, self.RULE_directConstructor)
        self._la = 0 # Token type
        try:
            self.state = 1487
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,126,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1484
                self.dirElemConstructorOpenClose()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1485
                self.dirElemConstructorSingleTag()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1486
                _la = self._input.LA(1)
                if not(_la==XQueryParser.COMMENT or _la==XQueryParser.PI):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirElemConstructorOpenCloseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.openName = None # QNameContext
            self.endOpen = None # Token
            self.startClose = None # Token
            self.slashClose = None # Token
            self.closeName = None # QNameContext

        def LANGLE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.LANGLE)
            else:
                return self.getToken(XQueryParser.LANGLE, i)

        def dirAttributeList(self):
            return self.getTypedRuleContext(XQueryParser.DirAttributeListContext,0)


        def RANGLE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.RANGLE)
            else:
                return self.getToken(XQueryParser.RANGLE, i)

        def qName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.QNameContext)
            else:
                return self.getTypedRuleContext(XQueryParser.QNameContext,i)


        def SLASH(self):
            return self.getToken(XQueryParser.SLASH, 0)

        def dirElemContent(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.DirElemContentContext)
            else:
                return self.getTypedRuleContext(XQueryParser.DirElemContentContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirElemConstructorOpenClose

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirElemConstructorOpenClose" ):
                listener.enterDirElemConstructorOpenClose(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirElemConstructorOpenClose" ):
                listener.exitDirElemConstructorOpenClose(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirElemConstructorOpenClose" ):
                return visitor.visitDirElemConstructorOpenClose(self)
            else:
                return visitor.visitChildren(self)




    def dirElemConstructorOpenClose(self):

        localctx = XQueryParser.DirElemConstructorOpenCloseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 278, self.RULE_dirElemConstructorOpenClose)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1489
            self.match(XQueryParser.LANGLE)
            self.state = 1490
            localctx.openName = self.qName()
            self.state = 1491
            self.dirAttributeList()
            self.state = 1492
            localctx.endOpen = self.match(XQueryParser.RANGLE)
            self.state = 1496
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,127,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1493
                    self.dirElemContent() 
                self.state = 1498
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,127,self._ctx)

            self.state = 1499
            localctx.startClose = self.match(XQueryParser.LANGLE)
            self.state = 1500
            localctx.slashClose = self.match(XQueryParser.SLASH)
            self.state = 1501
            localctx.closeName = self.qName()
            self.state = 1502
            self.match(XQueryParser.RANGLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirElemConstructorSingleTagContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.openName = None # QNameContext
            self.slashClose = None # Token

        def LANGLE(self):
            return self.getToken(XQueryParser.LANGLE, 0)

        def dirAttributeList(self):
            return self.getTypedRuleContext(XQueryParser.DirAttributeListContext,0)


        def RANGLE(self):
            return self.getToken(XQueryParser.RANGLE, 0)

        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def SLASH(self):
            return self.getToken(XQueryParser.SLASH, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_dirElemConstructorSingleTag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirElemConstructorSingleTag" ):
                listener.enterDirElemConstructorSingleTag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirElemConstructorSingleTag" ):
                listener.exitDirElemConstructorSingleTag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirElemConstructorSingleTag" ):
                return visitor.visitDirElemConstructorSingleTag(self)
            else:
                return visitor.visitChildren(self)




    def dirElemConstructorSingleTag(self):

        localctx = XQueryParser.DirElemConstructorSingleTagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 280, self.RULE_dirElemConstructorSingleTag)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1504
            self.match(XQueryParser.LANGLE)
            self.state = 1505
            localctx.openName = self.qName()
            self.state = 1506
            self.dirAttributeList()
            self.state = 1507
            localctx.slashClose = self.match(XQueryParser.SLASH)
            self.state = 1508
            self.match(XQueryParser.RANGLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirAttributeListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.QNameContext)
            else:
                return self.getTypedRuleContext(XQueryParser.QNameContext,i)


        def EQUAL(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EQUAL)
            else:
                return self.getToken(XQueryParser.EQUAL, i)

        def dirAttributeValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.DirAttributeValueContext)
            else:
                return self.getTypedRuleContext(XQueryParser.DirAttributeValueContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirAttributeList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirAttributeList" ):
                listener.enterDirAttributeList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirAttributeList" ):
                listener.exitDirAttributeList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirAttributeList" ):
                return visitor.visitDirAttributeList(self)
            else:
                return visitor.visitChildren(self)




    def dirAttributeList(self):

        localctx = XQueryParser.DirAttributeListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 282, self.RULE_dirAttributeList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1516
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ANCESTOR) | (1 << XQueryParser.KW_ANCESTOR_OR_SELF) | (1 << XQueryParser.KW_AND) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_AS) | (1 << XQueryParser.KW_ASCENDING) | (1 << XQueryParser.KW_AT) | (1 << XQueryParser.KW_ATTRIBUTE) | (1 << XQueryParser.KW_BASE_URI) | (1 << XQueryParser.KW_BOUNDARY_SPACE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_BY - 64)) | (1 << (XQueryParser.KW_CASE - 64)) | (1 << (XQueryParser.KW_CAST - 64)) | (1 << (XQueryParser.KW_CASTABLE - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_CHILD - 64)) | (1 << (XQueryParser.KW_COLLATION - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONSTRUCTION - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COPY_NS - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECLARE - 64)) | (1 << (XQueryParser.KW_DEFAULT - 64)) | (1 << (XQueryParser.KW_DESCENDANT - 64)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 64)) | (1 << (XQueryParser.KW_DESCENDING - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DIV - 64)) | (1 << (XQueryParser.KW_DOCUMENT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_ELSE - 64)) | (1 << (XQueryParser.KW_EMPTY - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_ENCODING - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_EQ - 64)) | (1 << (XQueryParser.KW_EVERY - 64)) | (1 << (XQueryParser.KW_EXCEPT - 64)) | (1 << (XQueryParser.KW_EXTERNAL - 64)) | (1 << (XQueryParser.KW_FOLLOWING - 64)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 64)) | (1 << (XQueryParser.KW_FOR - 64)) | (1 << (XQueryParser.KW_FUNCTION - 64)) | (1 << (XQueryParser.KW_GE - 64)) | (1 << (XQueryParser.KW_GREATEST - 64)) | (1 << (XQueryParser.KW_GROUP - 64)) | (1 << (XQueryParser.KW_GT - 64)) | (1 << (XQueryParser.KW_IDIV - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_IMPORT - 64)) | (1 << (XQueryParser.KW_IN - 64)) | (1 << (XQueryParser.KW_INHERIT - 64)) | (1 << (XQueryParser.KW_INSTANCE - 64)) | (1 << (XQueryParser.KW_INTERSECT - 64)) | (1 << (XQueryParser.KW_IS - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_LAX - 64)) | (1 << (XQueryParser.KW_LE - 64)) | (1 << (XQueryParser.KW_LEAST - 64)) | (1 << (XQueryParser.KW_LET - 64)) | (1 << (XQueryParser.KW_LT - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_MOD - 64)) | (1 << (XQueryParser.KW_MODULE - 64)) | (1 << (XQueryParser.KW_NAMESPACE - 64)) | (1 << (XQueryParser.KW_NE - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NO_INHERIT - 64)) | (1 << (XQueryParser.KW_NO_PRESERVE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (XQueryParser.KW_OF - 128)) | (1 << (XQueryParser.KW_ONLY - 128)) | (1 << (XQueryParser.KW_OPTION - 128)) | (1 << (XQueryParser.KW_OR - 128)) | (1 << (XQueryParser.KW_ORDER - 128)) | (1 << (XQueryParser.KW_ORDERED - 128)) | (1 << (XQueryParser.KW_ORDERING - 128)) | (1 << (XQueryParser.KW_PARENT - 128)) | (1 << (XQueryParser.KW_PRECEDING - 128)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 128)) | (1 << (XQueryParser.KW_PRESERVE - 128)) | (1 << (XQueryParser.KW_PI - 128)) | (1 << (XQueryParser.KW_RETURN - 128)) | (1 << (XQueryParser.KW_SATISFIES - 128)) | (1 << (XQueryParser.KW_SCHEMA - 128)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 128)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 128)) | (1 << (XQueryParser.KW_SELF - 128)) | (1 << (XQueryParser.KW_SLIDING - 128)) | (1 << (XQueryParser.KW_SOME - 128)) | (1 << (XQueryParser.KW_STABLE - 128)) | (1 << (XQueryParser.KW_START - 128)) | (1 << (XQueryParser.KW_STRICT - 128)) | (1 << (XQueryParser.KW_STRIP - 128)) | (1 << (XQueryParser.KW_SWITCH - 128)) | (1 << (XQueryParser.KW_TEXT - 128)) | (1 << (XQueryParser.KW_THEN - 128)) | (1 << (XQueryParser.KW_TO - 128)) | (1 << (XQueryParser.KW_TREAT - 128)) | (1 << (XQueryParser.KW_TRY - 128)) | (1 << (XQueryParser.KW_TUMBLING - 128)) | (1 << (XQueryParser.KW_TYPE - 128)) | (1 << (XQueryParser.KW_TYPESWITCH - 128)) | (1 << (XQueryParser.KW_UNION - 128)) | (1 << (XQueryParser.KW_UNORDERED - 128)) | (1 << (XQueryParser.KW_UPDATE - 128)) | (1 << (XQueryParser.KW_VALIDATE - 128)) | (1 << (XQueryParser.KW_VARIABLE - 128)) | (1 << (XQueryParser.KW_VERSION - 128)) | (1 << (XQueryParser.KW_WHEN - 128)) | (1 << (XQueryParser.KW_WHERE - 128)) | (1 << (XQueryParser.KW_WINDOW - 128)) | (1 << (XQueryParser.KW_XQUERY - 128)) | (1 << (XQueryParser.KW_ARRAY_NODE - 128)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 128)) | (1 << (XQueryParser.KW_NULL_NODE - 128)) | (1 << (XQueryParser.KW_NUMBER_NODE - 128)) | (1 << (XQueryParser.KW_OBJECT_NODE - 128)) | (1 << (XQueryParser.KW_REPLACE - 128)) | (1 << (XQueryParser.KW_WITH - 128)) | (1 << (XQueryParser.KW_VALUE - 128)) | (1 << (XQueryParser.KW_INSERT - 128)) | (1 << (XQueryParser.KW_INTO - 128)) | (1 << (XQueryParser.KW_DELETE - 128)) | (1 << (XQueryParser.KW_RENAME - 128)) | (1 << (XQueryParser.FullQName - 128)) | (1 << (XQueryParser.NCName - 128)))) != 0):
                self.state = 1510
                self.qName()
                self.state = 1511
                self.match(XQueryParser.EQUAL)
                self.state = 1512
                self.dirAttributeValue()
                self.state = 1518
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirAttributeValueAposContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Quot(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.Quot)
            else:
                return self.getToken(XQueryParser.Quot, i)

        def PredefinedEntityRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PredefinedEntityRef)
            else:
                return self.getToken(XQueryParser.PredefinedEntityRef, i)

        def CharRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.CharRef)
            else:
                return self.getToken(XQueryParser.CharRef, i)

        def EscapeQuot(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EscapeQuot)
            else:
                return self.getToken(XQueryParser.EscapeQuot, i)

        def dirAttributeContentQuot(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.DirAttributeContentQuotContext)
            else:
                return self.getTypedRuleContext(XQueryParser.DirAttributeContentQuotContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirAttributeValueApos

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirAttributeValueApos" ):
                listener.enterDirAttributeValueApos(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirAttributeValueApos" ):
                listener.exitDirAttributeValueApos(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirAttributeValueApos" ):
                return visitor.visitDirAttributeValueApos(self)
            else:
                return visitor.visitChildren(self)




    def dirAttributeValueApos(self):

        localctx = XQueryParser.DirAttributeValueAposContext(self, self._ctx, self.state)
        self.enterRule(localctx, 284, self.RULE_dirAttributeValueApos)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1519
            self.match(XQueryParser.Quot)
            self.state = 1526
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,130,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1524
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [XQueryParser.PredefinedEntityRef]:
                        self.state = 1520
                        self.match(XQueryParser.PredefinedEntityRef)
                        pass
                    elif token in [XQueryParser.CharRef]:
                        self.state = 1521
                        self.match(XQueryParser.CharRef)
                        pass
                    elif token in [XQueryParser.EscapeQuot]:
                        self.state = 1522
                        self.match(XQueryParser.EscapeQuot)
                        pass
                    elif token in [XQueryParser.DOUBLE_LBRACE, XQueryParser.DOUBLE_RBRACE, XQueryParser.Quot, XQueryParser.LBRACE, XQueryParser.ContentChar]:
                        self.state = 1523
                        self.dirAttributeContentQuot()
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 1528
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,130,self._ctx)

            self.state = 1529
            self.match(XQueryParser.Quot)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirAttributeValueQuotContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Apos(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.Apos)
            else:
                return self.getToken(XQueryParser.Apos, i)

        def PredefinedEntityRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PredefinedEntityRef)
            else:
                return self.getToken(XQueryParser.PredefinedEntityRef, i)

        def CharRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.CharRef)
            else:
                return self.getToken(XQueryParser.CharRef, i)

        def EscapeApos(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EscapeApos)
            else:
                return self.getToken(XQueryParser.EscapeApos, i)

        def dirAttributeContentApos(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.DirAttributeContentAposContext)
            else:
                return self.getTypedRuleContext(XQueryParser.DirAttributeContentAposContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirAttributeValueQuot

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirAttributeValueQuot" ):
                listener.enterDirAttributeValueQuot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirAttributeValueQuot" ):
                listener.exitDirAttributeValueQuot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirAttributeValueQuot" ):
                return visitor.visitDirAttributeValueQuot(self)
            else:
                return visitor.visitChildren(self)




    def dirAttributeValueQuot(self):

        localctx = XQueryParser.DirAttributeValueQuotContext(self, self._ctx, self.state)
        self.enterRule(localctx, 286, self.RULE_dirAttributeValueQuot)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1531
            self.match(XQueryParser.Apos)
            self.state = 1538
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,132,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 1536
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [XQueryParser.PredefinedEntityRef]:
                        self.state = 1532
                        self.match(XQueryParser.PredefinedEntityRef)
                        pass
                    elif token in [XQueryParser.CharRef]:
                        self.state = 1533
                        self.match(XQueryParser.CharRef)
                        pass
                    elif token in [XQueryParser.EscapeApos]:
                        self.state = 1534
                        self.match(XQueryParser.EscapeApos)
                        pass
                    elif token in [XQueryParser.DOUBLE_LBRACE, XQueryParser.DOUBLE_RBRACE, XQueryParser.Apos, XQueryParser.LBRACE, XQueryParser.ContentChar]:
                        self.state = 1535
                        self.dirAttributeContentApos()
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 1540
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,132,self._ctx)

            self.state = 1541
            self.match(XQueryParser.Apos)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirAttributeValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dirAttributeValueApos(self):
            return self.getTypedRuleContext(XQueryParser.DirAttributeValueAposContext,0)


        def dirAttributeValueQuot(self):
            return self.getTypedRuleContext(XQueryParser.DirAttributeValueQuotContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirAttributeValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirAttributeValue" ):
                listener.enterDirAttributeValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirAttributeValue" ):
                listener.exitDirAttributeValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirAttributeValue" ):
                return visitor.visitDirAttributeValue(self)
            else:
                return visitor.visitChildren(self)




    def dirAttributeValue(self):

        localctx = XQueryParser.DirAttributeValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 288, self.RULE_dirAttributeValue)
        try:
            self.state = 1545
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.Quot]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1543
                self.dirAttributeValueApos()
                pass
            elif token in [XQueryParser.Apos]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1544
                self.dirAttributeValueQuot()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirAttributeContentQuotContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ContentChar(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ContentChar)
            else:
                return self.getToken(XQueryParser.ContentChar, i)

        def DOUBLE_LBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_LBRACE, 0)

        def DOUBLE_RBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_RBRACE, 0)

        def dirAttributeValueApos(self):
            return self.getTypedRuleContext(XQueryParser.DirAttributeValueAposContext,0)


        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirAttributeContentQuot

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirAttributeContentQuot" ):
                listener.enterDirAttributeContentQuot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirAttributeContentQuot" ):
                listener.exitDirAttributeContentQuot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirAttributeContentQuot" ):
                return visitor.visitDirAttributeContentQuot(self)
            else:
                return visitor.visitChildren(self)




    def dirAttributeContentQuot(self):

        localctx = XQueryParser.DirAttributeContentQuotContext(self, self._ctx, self.state)
        self.enterRule(localctx, 290, self.RULE_dirAttributeContentQuot)
        self._la = 0 # Token type
        try:
            self.state = 1560
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.ContentChar]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1548 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1547
                        self.match(XQueryParser.ContentChar)

                    else:
                        raise NoViableAltException(self)
                    self.state = 1550 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,134,self._ctx)

                pass
            elif token in [XQueryParser.DOUBLE_LBRACE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1552
                self.match(XQueryParser.DOUBLE_LBRACE)
                pass
            elif token in [XQueryParser.DOUBLE_RBRACE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1553
                self.match(XQueryParser.DOUBLE_RBRACE)
                pass
            elif token in [XQueryParser.Quot]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1554
                self.dirAttributeValueApos()
                pass
            elif token in [XQueryParser.LBRACE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1555
                self.match(XQueryParser.LBRACE)
                self.state = 1557
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                    self.state = 1556
                    self.expr()


                self.state = 1559
                self.match(XQueryParser.RBRACE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirAttributeContentAposContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ContentChar(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ContentChar)
            else:
                return self.getToken(XQueryParser.ContentChar, i)

        def DOUBLE_LBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_LBRACE, 0)

        def DOUBLE_RBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_RBRACE, 0)

        def dirAttributeValueQuot(self):
            return self.getTypedRuleContext(XQueryParser.DirAttributeValueQuotContext,0)


        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirAttributeContentApos

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirAttributeContentApos" ):
                listener.enterDirAttributeContentApos(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirAttributeContentApos" ):
                listener.exitDirAttributeContentApos(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirAttributeContentApos" ):
                return visitor.visitDirAttributeContentApos(self)
            else:
                return visitor.visitChildren(self)




    def dirAttributeContentApos(self):

        localctx = XQueryParser.DirAttributeContentAposContext(self, self._ctx, self.state)
        self.enterRule(localctx, 292, self.RULE_dirAttributeContentApos)
        self._la = 0 # Token type
        try:
            self.state = 1575
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.ContentChar]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1563 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1562
                        self.match(XQueryParser.ContentChar)

                    else:
                        raise NoViableAltException(self)
                    self.state = 1565 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,137,self._ctx)

                pass
            elif token in [XQueryParser.DOUBLE_LBRACE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1567
                self.match(XQueryParser.DOUBLE_LBRACE)
                pass
            elif token in [XQueryParser.DOUBLE_RBRACE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1568
                self.match(XQueryParser.DOUBLE_RBRACE)
                pass
            elif token in [XQueryParser.Apos]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1569
                self.dirAttributeValueQuot()
                pass
            elif token in [XQueryParser.LBRACE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1570
                self.match(XQueryParser.LBRACE)
                self.state = 1572
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                    self.state = 1571
                    self.expr()


                self.state = 1574
                self.match(XQueryParser.RBRACE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirElemContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def directConstructor(self):
            return self.getTypedRuleContext(XQueryParser.DirectConstructorContext,0)


        def commonContent(self):
            return self.getTypedRuleContext(XQueryParser.CommonContentContext,0)


        def CDATA(self):
            return self.getToken(XQueryParser.CDATA, 0)

        def Quot(self):
            return self.getToken(XQueryParser.Quot, 0)

        def Apos(self):
            return self.getToken(XQueryParser.Apos, 0)

        def noQuotesNoBracesNoAmpNoLAng(self):
            return self.getTypedRuleContext(XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_dirElemContent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirElemContent" ):
                listener.enterDirElemContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirElemContent" ):
                listener.exitDirElemContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirElemContent" ):
                return visitor.visitDirElemContent(self)
            else:
                return visitor.visitChildren(self)




    def dirElemContent(self):

        localctx = XQueryParser.DirElemContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 294, self.RULE_dirElemContent)
        try:
            self.state = 1583
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,140,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1577
                self.directConstructor()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1578
                self.commonContent()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1579
                self.match(XQueryParser.CDATA)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1580
                self.match(XQueryParser.Quot)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1581
                self.match(XQueryParser.Apos)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1582
                self.noQuotesNoBracesNoAmpNoLAng()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommonContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PredefinedEntityRef(self):
            return self.getToken(XQueryParser.PredefinedEntityRef, 0)

        def CharRef(self):
            return self.getToken(XQueryParser.CharRef, 0)

        def LBRACE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.LBRACE)
            else:
                return self.getToken(XQueryParser.LBRACE, i)

        def RBRACE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.RBRACE)
            else:
                return self.getToken(XQueryParser.RBRACE, i)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_commonContent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommonContent" ):
                listener.enterCommonContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommonContent" ):
                listener.exitCommonContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommonContent" ):
                return visitor.visitCommonContent(self)
            else:
                return visitor.visitChildren(self)




    def commonContent(self):

        localctx = XQueryParser.CommonContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 296, self.RULE_commonContent)
        self._la = 0 # Token type
        try:
            self.state = 1594
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,141,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1585
                _la = self._input.LA(1)
                if not(_la==XQueryParser.PredefinedEntityRef or _la==XQueryParser.CharRef):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1586
                self.match(XQueryParser.LBRACE)
                self.state = 1587
                self.match(XQueryParser.LBRACE)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1588
                self.match(XQueryParser.RBRACE)
                self.state = 1589
                self.match(XQueryParser.RBRACE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1590
                self.match(XQueryParser.LBRACE)
                self.state = 1591
                self.expr()
                self.state = 1592
                self.match(XQueryParser.RBRACE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComputedConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def compDocConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompDocConstructorContext,0)


        def compElemConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompElemConstructorContext,0)


        def compAttrConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompAttrConstructorContext,0)


        def compNamespaceConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompNamespaceConstructorContext,0)


        def compTextConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompTextConstructorContext,0)


        def compCommentConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompCommentConstructorContext,0)


        def compPIConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompPIConstructorContext,0)


        def compMLJSONConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompMLJSONConstructorContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_computedConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComputedConstructor" ):
                listener.enterComputedConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComputedConstructor" ):
                listener.exitComputedConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComputedConstructor" ):
                return visitor.visitComputedConstructor(self)
            else:
                return visitor.visitChildren(self)




    def computedConstructor(self):

        localctx = XQueryParser.ComputedConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 298, self.RULE_computedConstructor)
        try:
            self.state = 1604
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_DOCUMENT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1596
                self.compDocConstructor()
                pass
            elif token in [XQueryParser.KW_ELEMENT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1597
                self.compElemConstructor()
                pass
            elif token in [XQueryParser.KW_ATTRIBUTE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1598
                self.compAttrConstructor()
                pass
            elif token in [XQueryParser.KW_NAMESPACE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1599
                self.compNamespaceConstructor()
                pass
            elif token in [XQueryParser.KW_TEXT]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1600
                self.compTextConstructor()
                pass
            elif token in [XQueryParser.KW_COMMENT]:
                self.enterOuterAlt(localctx, 6)
                self.state = 1601
                self.compCommentConstructor()
                pass
            elif token in [XQueryParser.KW_PI]:
                self.enterOuterAlt(localctx, 7)
                self.state = 1602
                self.compPIConstructor()
                pass
            elif token in [XQueryParser.KW_BINARY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 1603
                self.compMLJSONConstructor()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompMLJSONConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def compMLJSONArrayConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompMLJSONArrayConstructorContext,0)


        def compMLJSONObjectConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompMLJSONObjectConstructorContext,0)


        def compMLJSONNumberConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompMLJSONNumberConstructorContext,0)


        def compMLJSONBooleanConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompMLJSONBooleanConstructorContext,0)


        def compMLJSONNullConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompMLJSONNullConstructorContext,0)


        def compBinaryConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CompBinaryConstructorContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compMLJSONConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompMLJSONConstructor" ):
                listener.enterCompMLJSONConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompMLJSONConstructor" ):
                listener.exitCompMLJSONConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompMLJSONConstructor" ):
                return visitor.visitCompMLJSONConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compMLJSONConstructor(self):

        localctx = XQueryParser.CompMLJSONConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 300, self.RULE_compMLJSONConstructor)
        try:
            self.state = 1612
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_ARRAY_NODE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1606
                self.compMLJSONArrayConstructor()
                pass
            elif token in [XQueryParser.KW_OBJECT_NODE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1607
                self.compMLJSONObjectConstructor()
                pass
            elif token in [XQueryParser.KW_NUMBER_NODE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1608
                self.compMLJSONNumberConstructor()
                pass
            elif token in [XQueryParser.KW_BOOLEAN_NODE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1609
                self.compMLJSONBooleanConstructor()
                pass
            elif token in [XQueryParser.KW_NULL_NODE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1610
                self.compMLJSONNullConstructor()
                pass
            elif token in [XQueryParser.KW_BINARY]:
                self.enterOuterAlt(localctx, 6)
                self.state = 1611
                self.compBinaryConstructor()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompMLJSONArrayConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ARRAY_NODE(self):
            return self.getToken(XQueryParser.KW_ARRAY_NODE, 0)

        def enclosedContentExpr(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedContentExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compMLJSONArrayConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompMLJSONArrayConstructor" ):
                listener.enterCompMLJSONArrayConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompMLJSONArrayConstructor" ):
                listener.exitCompMLJSONArrayConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompMLJSONArrayConstructor" ):
                return visitor.visitCompMLJSONArrayConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compMLJSONArrayConstructor(self):

        localctx = XQueryParser.CompMLJSONArrayConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 302, self.RULE_compMLJSONArrayConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1614
            self.match(XQueryParser.KW_ARRAY_NODE)
            self.state = 1615
            self.enclosedContentExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompMLJSONObjectConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_OBJECT_NODE(self):
            return self.getToken(XQueryParser.KW_OBJECT_NODE, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COLON)
            else:
                return self.getToken(XQueryParser.COLON, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_compMLJSONObjectConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompMLJSONObjectConstructor" ):
                listener.enterCompMLJSONObjectConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompMLJSONObjectConstructor" ):
                listener.exitCompMLJSONObjectConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompMLJSONObjectConstructor" ):
                return visitor.visitCompMLJSONObjectConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compMLJSONObjectConstructor(self):

        localctx = XQueryParser.CompMLJSONObjectConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 304, self.RULE_compMLJSONObjectConstructor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1617
            self.match(XQueryParser.KW_OBJECT_NODE)
            self.state = 1618
            self.match(XQueryParser.LBRACE)
            self.state = 1632
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                self.state = 1619
                self.exprSingle()
                self.state = 1620
                self.match(XQueryParser.COLON)
                self.state = 1621
                self.exprSingle()
                self.state = 1629
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 1622
                    self.match(XQueryParser.COMMA)
                    self.state = 1623
                    self.exprSingle()
                    self.state = 1624
                    self.match(XQueryParser.COLON)
                    self.state = 1625
                    self.exprSingle()
                    self.state = 1631
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 1634
            self.match(XQueryParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompMLJSONNumberConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NUMBER_NODE(self):
            return self.getToken(XQueryParser.KW_NUMBER_NODE, 0)

        def enclosedContentExpr(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedContentExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compMLJSONNumberConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompMLJSONNumberConstructor" ):
                listener.enterCompMLJSONNumberConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompMLJSONNumberConstructor" ):
                listener.exitCompMLJSONNumberConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompMLJSONNumberConstructor" ):
                return visitor.visitCompMLJSONNumberConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compMLJSONNumberConstructor(self):

        localctx = XQueryParser.CompMLJSONNumberConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 306, self.RULE_compMLJSONNumberConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1636
            self.match(XQueryParser.KW_NUMBER_NODE)
            self.state = 1637
            self.enclosedContentExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompMLJSONBooleanConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_BOOLEAN_NODE(self):
            return self.getToken(XQueryParser.KW_BOOLEAN_NODE, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def exprSingle(self):
            return self.getTypedRuleContext(XQueryParser.ExprSingleContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_compMLJSONBooleanConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompMLJSONBooleanConstructor" ):
                listener.enterCompMLJSONBooleanConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompMLJSONBooleanConstructor" ):
                listener.exitCompMLJSONBooleanConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompMLJSONBooleanConstructor" ):
                return visitor.visitCompMLJSONBooleanConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compMLJSONBooleanConstructor(self):

        localctx = XQueryParser.CompMLJSONBooleanConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 308, self.RULE_compMLJSONBooleanConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1639
            self.match(XQueryParser.KW_BOOLEAN_NODE)
            self.state = 1640
            self.match(XQueryParser.LBRACE)
            self.state = 1641
            self.exprSingle()
            self.state = 1642
            self.match(XQueryParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompMLJSONNullConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NULL_NODE(self):
            return self.getToken(XQueryParser.KW_NULL_NODE, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_compMLJSONNullConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompMLJSONNullConstructor" ):
                listener.enterCompMLJSONNullConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompMLJSONNullConstructor" ):
                listener.exitCompMLJSONNullConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompMLJSONNullConstructor" ):
                return visitor.visitCompMLJSONNullConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compMLJSONNullConstructor(self):

        localctx = XQueryParser.CompMLJSONNullConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 310, self.RULE_compMLJSONNullConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1644
            self.match(XQueryParser.KW_NULL_NODE)
            self.state = 1645
            self.match(XQueryParser.LBRACE)
            self.state = 1646
            self.match(XQueryParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompBinaryConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_BINARY(self):
            return self.getToken(XQueryParser.KW_BINARY, 0)

        def enclosedContentExpr(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedContentExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compBinaryConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompBinaryConstructor" ):
                listener.enterCompBinaryConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompBinaryConstructor" ):
                listener.exitCompBinaryConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompBinaryConstructor" ):
                return visitor.visitCompBinaryConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compBinaryConstructor(self):

        localctx = XQueryParser.CompBinaryConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 312, self.RULE_compBinaryConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1648
            self.match(XQueryParser.KW_BINARY)
            self.state = 1649
            self.enclosedContentExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompDocConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DOCUMENT(self):
            return self.getToken(XQueryParser.KW_DOCUMENT, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compDocConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompDocConstructor" ):
                listener.enterCompDocConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompDocConstructor" ):
                listener.exitCompDocConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompDocConstructor" ):
                return visitor.visitCompDocConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compDocConstructor(self):

        localctx = XQueryParser.CompDocConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 314, self.RULE_compDocConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1651
            self.match(XQueryParser.KW_DOCUMENT)
            self.state = 1652
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompElemConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ELEMENT(self):
            return self.getToken(XQueryParser.KW_ELEMENT, 0)

        def enclosedContentExpr(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedContentExprContext,0)


        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_compElemConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompElemConstructor" ):
                listener.enterCompElemConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompElemConstructor" ):
                listener.exitCompElemConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompElemConstructor" ):
                return visitor.visitCompElemConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compElemConstructor(self):

        localctx = XQueryParser.CompElemConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 316, self.RULE_compElemConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1654
            self.match(XQueryParser.KW_ELEMENT)
            self.state = 1660
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCName]:
                self.state = 1655
                self.eqName()
                pass
            elif token in [XQueryParser.LBRACE]:
                self.state = 1656
                self.match(XQueryParser.LBRACE)
                self.state = 1657
                self.expr()
                self.state = 1658
                self.match(XQueryParser.RBRACE)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 1662
            self.enclosedContentExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnclosedContentExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_enclosedContentExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnclosedContentExpr" ):
                listener.enterEnclosedContentExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnclosedContentExpr" ):
                listener.exitEnclosedContentExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnclosedContentExpr" ):
                return visitor.visitEnclosedContentExpr(self)
            else:
                return visitor.visitChildren(self)




    def enclosedContentExpr(self):

        localctx = XQueryParser.EnclosedContentExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 318, self.RULE_enclosedContentExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1664
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompAttrConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ATTRIBUTE(self):
            return self.getToken(XQueryParser.KW_ATTRIBUTE, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_compAttrConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompAttrConstructor" ):
                listener.enterCompAttrConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompAttrConstructor" ):
                listener.exitCompAttrConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompAttrConstructor" ):
                return visitor.visitCompAttrConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compAttrConstructor(self):

        localctx = XQueryParser.CompAttrConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 320, self.RULE_compAttrConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1666
            self.match(XQueryParser.KW_ATTRIBUTE)
            self.state = 1672
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCName]:
                self.state = 1667
                self.eqName()
                pass
            elif token in [XQueryParser.LBRACE]:
                self.state = 1668
                self.match(XQueryParser.LBRACE)
                self.state = 1669
                self.expr()
                self.state = 1670
                self.match(XQueryParser.RBRACE)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 1674
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompNamespaceConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def enclosedURIExpr(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedURIExprContext,0)


        def prefix(self):
            return self.getTypedRuleContext(XQueryParser.PrefixContext,0)


        def enclosedPrefixExpr(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedPrefixExprContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compNamespaceConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompNamespaceConstructor" ):
                listener.enterCompNamespaceConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompNamespaceConstructor" ):
                listener.exitCompNamespaceConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompNamespaceConstructor" ):
                return visitor.visitCompNamespaceConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compNamespaceConstructor(self):

        localctx = XQueryParser.CompNamespaceConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 322, self.RULE_compNamespaceConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1676
            self.match(XQueryParser.KW_NAMESPACE)
            self.state = 1679
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.NCName]:
                self.state = 1677
                self.prefix()
                pass
            elif token in [XQueryParser.LBRACE]:
                self.state = 1678
                self.enclosedPrefixExpr()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 1681
            self.enclosedURIExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrefixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_prefix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefix" ):
                listener.enterPrefix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefix" ):
                listener.exitPrefix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefix" ):
                return visitor.visitPrefix(self)
            else:
                return visitor.visitChildren(self)




    def prefix(self):

        localctx = XQueryParser.PrefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 324, self.RULE_prefix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1683
            self.ncName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnclosedPrefixExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_enclosedPrefixExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnclosedPrefixExpr" ):
                listener.enterEnclosedPrefixExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnclosedPrefixExpr" ):
                listener.exitEnclosedPrefixExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnclosedPrefixExpr" ):
                return visitor.visitEnclosedPrefixExpr(self)
            else:
                return visitor.visitChildren(self)




    def enclosedPrefixExpr(self):

        localctx = XQueryParser.EnclosedPrefixExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 326, self.RULE_enclosedPrefixExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1685
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnclosedURIExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_enclosedURIExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnclosedURIExpr" ):
                listener.enterEnclosedURIExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnclosedURIExpr" ):
                listener.exitEnclosedURIExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnclosedURIExpr" ):
                return visitor.visitEnclosedURIExpr(self)
            else:
                return visitor.visitChildren(self)




    def enclosedURIExpr(self):

        localctx = XQueryParser.EnclosedURIExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 328, self.RULE_enclosedURIExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1687
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompTextConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_TEXT(self):
            return self.getToken(XQueryParser.KW_TEXT, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compTextConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompTextConstructor" ):
                listener.enterCompTextConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompTextConstructor" ):
                listener.exitCompTextConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompTextConstructor" ):
                return visitor.visitCompTextConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compTextConstructor(self):

        localctx = XQueryParser.CompTextConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 330, self.RULE_compTextConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1689
            self.match(XQueryParser.KW_TEXT)
            self.state = 1690
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompCommentConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_COMMENT(self):
            return self.getToken(XQueryParser.KW_COMMENT, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_compCommentConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompCommentConstructor" ):
                listener.enterCompCommentConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompCommentConstructor" ):
                listener.exitCompCommentConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompCommentConstructor" ):
                return visitor.visitCompCommentConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compCommentConstructor(self):

        localctx = XQueryParser.CompCommentConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 332, self.RULE_compCommentConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1692
            self.match(XQueryParser.KW_COMMENT)
            self.state = 1693
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompPIConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_PI(self):
            return self.getToken(XQueryParser.KW_PI, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_compPIConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompPIConstructor" ):
                listener.enterCompPIConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompPIConstructor" ):
                listener.exitCompPIConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompPIConstructor" ):
                return visitor.visitCompPIConstructor(self)
            else:
                return visitor.visitChildren(self)




    def compPIConstructor(self):

        localctx = XQueryParser.CompPIConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 334, self.RULE_compPIConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1695
            self.match(XQueryParser.KW_PI)
            self.state = 1701
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.NCName]:
                self.state = 1696
                self.ncName()
                pass
            elif token in [XQueryParser.LBRACE]:
                self.state = 1697
                self.match(XQueryParser.LBRACE)
                self.state = 1698
                self.expr()
                self.state = 1699
                self.match(XQueryParser.RBRACE)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 1703
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionItemExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def namedFunctionRef(self):
            return self.getTypedRuleContext(XQueryParser.NamedFunctionRefContext,0)


        def inlineFunctionRef(self):
            return self.getTypedRuleContext(XQueryParser.InlineFunctionRefContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionItemExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionItemExpr" ):
                listener.enterFunctionItemExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionItemExpr" ):
                listener.exitFunctionItemExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionItemExpr" ):
                return visitor.visitFunctionItemExpr(self)
            else:
                return visitor.visitChildren(self)




    def functionItemExpr(self):

        localctx = XQueryParser.FunctionItemExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 336, self.RULE_functionItemExpr)
        try:
            self.state = 1707
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,150,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1705
                self.namedFunctionRef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1706
                self.inlineFunctionRef()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamedFunctionRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def HASH(self):
            return self.getToken(XQueryParser.HASH, 0)

        def IntegerLiteral(self):
            return self.getToken(XQueryParser.IntegerLiteral, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_namedFunctionRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamedFunctionRef" ):
                listener.enterNamedFunctionRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamedFunctionRef" ):
                listener.exitNamedFunctionRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedFunctionRef" ):
                return visitor.visitNamedFunctionRef(self)
            else:
                return visitor.visitChildren(self)




    def namedFunctionRef(self):

        localctx = XQueryParser.NamedFunctionRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 338, self.RULE_namedFunctionRef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1709
            self.eqName()
            self.state = 1710
            self.match(XQueryParser.HASH)
            self.state = 1711
            self.match(XQueryParser.IntegerLiteral)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InlineFunctionRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def annotations(self):
            return self.getTypedRuleContext(XQueryParser.AnnotationsContext,0)


        def KW_FUNCTION(self):
            return self.getToken(XQueryParser.KW_FUNCTION, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def functionBody(self):
            return self.getTypedRuleContext(XQueryParser.FunctionBodyContext,0)


        def functionParams(self):
            return self.getTypedRuleContext(XQueryParser.FunctionParamsContext,0)


        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_inlineFunctionRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInlineFunctionRef" ):
                listener.enterInlineFunctionRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInlineFunctionRef" ):
                listener.exitInlineFunctionRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInlineFunctionRef" ):
                return visitor.visitInlineFunctionRef(self)
            else:
                return visitor.visitChildren(self)




    def inlineFunctionRef(self):

        localctx = XQueryParser.InlineFunctionRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 340, self.RULE_inlineFunctionRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1713
            self.annotations()
            self.state = 1714
            self.match(XQueryParser.KW_FUNCTION)
            self.state = 1715
            self.match(XQueryParser.LPAREN)
            self.state = 1717
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.DOLLAR:
                self.state = 1716
                self.functionParams()


            self.state = 1719
            self.match(XQueryParser.RPAREN)
            self.state = 1722
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.KW_AS:
                self.state = 1720
                self.match(XQueryParser.KW_AS)
                self.state = 1721
                self.sequenceType()


            self.state = 1724
            self.functionBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionBody" ):
                listener.enterFunctionBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionBody" ):
                listener.exitFunctionBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionBody" ):
                return visitor.visitFunctionBody(self)
            else:
                return visitor.visitChildren(self)




    def functionBody(self):

        localctx = XQueryParser.FunctionBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 342, self.RULE_functionBody)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1726
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MapConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_MAP(self):
            return self.getToken(XQueryParser.KW_MAP, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def mapConstructorEntry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.MapConstructorEntryContext)
            else:
                return self.getTypedRuleContext(XQueryParser.MapConstructorEntryContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_mapConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMapConstructor" ):
                listener.enterMapConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMapConstructor" ):
                listener.exitMapConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMapConstructor" ):
                return visitor.visitMapConstructor(self)
            else:
                return visitor.visitChildren(self)




    def mapConstructor(self):

        localctx = XQueryParser.MapConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 344, self.RULE_mapConstructor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1728
            self.match(XQueryParser.KW_MAP)
            self.state = 1729
            self.match(XQueryParser.LBRACE)
            self.state = 1738
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                self.state = 1730
                self.mapConstructorEntry()
                self.state = 1735
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 1731
                    self.match(XQueryParser.COMMA)
                    self.state = 1732
                    self.mapConstructorEntry()
                    self.state = 1737
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 1740
            self.match(XQueryParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MapConstructorEntryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.mapKey = None # ExprSingleContext
            self.mapValue = None # ExprSingleContext

        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def COLON(self):
            return self.getToken(XQueryParser.COLON, 0)

        def COLON_EQ(self):
            return self.getToken(XQueryParser.COLON_EQ, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_mapConstructorEntry

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMapConstructorEntry" ):
                listener.enterMapConstructorEntry(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMapConstructorEntry" ):
                listener.exitMapConstructorEntry(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMapConstructorEntry" ):
                return visitor.visitMapConstructorEntry(self)
            else:
                return visitor.visitChildren(self)




    def mapConstructorEntry(self):

        localctx = XQueryParser.MapConstructorEntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 346, self.RULE_mapConstructorEntry)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1742
            localctx.mapKey = self.exprSingle()
            self.state = 1743
            _la = self._input.LA(1)
            if not(_la==XQueryParser.COLON or _la==XQueryParser.COLON_EQ):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 1744
            localctx.mapValue = self.exprSingle()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def squareArrayConstructor(self):
            return self.getTypedRuleContext(XQueryParser.SquareArrayConstructorContext,0)


        def curlyArrayConstructor(self):
            return self.getTypedRuleContext(XQueryParser.CurlyArrayConstructorContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_arrayConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayConstructor" ):
                listener.enterArrayConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayConstructor" ):
                listener.exitArrayConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayConstructor" ):
                return visitor.visitArrayConstructor(self)
            else:
                return visitor.visitChildren(self)




    def arrayConstructor(self):

        localctx = XQueryParser.ArrayConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 348, self.RULE_arrayConstructor)
        try:
            self.state = 1748
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.LBRACKET]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1746
                self.squareArrayConstructor()
                pass
            elif token in [XQueryParser.KW_ARRAY]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1747
                self.curlyArrayConstructor()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SquareArrayConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(XQueryParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(XQueryParser.RBRACKET, 0)

        def exprSingle(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.ExprSingleContext)
            else:
                return self.getTypedRuleContext(XQueryParser.ExprSingleContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_squareArrayConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSquareArrayConstructor" ):
                listener.enterSquareArrayConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSquareArrayConstructor" ):
                listener.exitSquareArrayConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSquareArrayConstructor" ):
                return visitor.visitSquareArrayConstructor(self)
            else:
                return visitor.visitChildren(self)




    def squareArrayConstructor(self):

        localctx = XQueryParser.SquareArrayConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 350, self.RULE_squareArrayConstructor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1750
            self.match(XQueryParser.LBRACKET)
            self.state = 1759
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 5)) & ~0x3f) == 0 and ((1 << (_la - 5)) & ((1 << (XQueryParser.IntegerLiteral - 5)) | (1 << (XQueryParser.DecimalLiteral - 5)) | (1 << (XQueryParser.DoubleLiteral - 5)) | (1 << (XQueryParser.DFPropertyName - 5)) | (1 << (XQueryParser.Quot - 5)) | (1 << (XQueryParser.Apos - 5)) | (1 << (XQueryParser.COMMENT - 5)) | (1 << (XQueryParser.PI - 5)) | (1 << (XQueryParser.PRAGMA - 5)) | (1 << (XQueryParser.LPAREN - 5)) | (1 << (XQueryParser.LBRACKET - 5)) | (1 << (XQueryParser.STAR - 5)) | (1 << (XQueryParser.PLUS - 5)) | (1 << (XQueryParser.MINUS - 5)) | (1 << (XQueryParser.DOT - 5)) | (1 << (XQueryParser.DDOT - 5)) | (1 << (XQueryParser.SLASH - 5)) | (1 << (XQueryParser.DSLASH - 5)) | (1 << (XQueryParser.LANGLE - 5)) | (1 << (XQueryParser.QUESTION - 5)) | (1 << (XQueryParser.AT - 5)) | (1 << (XQueryParser.DOLLAR - 5)) | (1 << (XQueryParser.MOD - 5)) | (1 << (XQueryParser.KW_ALLOWING - 5)) | (1 << (XQueryParser.KW_ANCESTOR - 5)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 5)) | (1 << (XQueryParser.KW_AND - 5)) | (1 << (XQueryParser.KW_ARRAY - 5)) | (1 << (XQueryParser.KW_AS - 5)) | (1 << (XQueryParser.KW_ASCENDING - 5)) | (1 << (XQueryParser.KW_AT - 5)) | (1 << (XQueryParser.KW_ATTRIBUTE - 5)) | (1 << (XQueryParser.KW_BASE_URI - 5)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 5)) | (1 << (XQueryParser.KW_BINARY - 5)) | (1 << (XQueryParser.KW_BY - 5)) | (1 << (XQueryParser.KW_CASE - 5)) | (1 << (XQueryParser.KW_CAST - 5)) | (1 << (XQueryParser.KW_CASTABLE - 5)))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (XQueryParser.KW_CATCH - 69)) | (1 << (XQueryParser.KW_CHILD - 69)) | (1 << (XQueryParser.KW_COLLATION - 69)) | (1 << (XQueryParser.KW_COMMENT - 69)) | (1 << (XQueryParser.KW_CONSTRUCTION - 69)) | (1 << (XQueryParser.KW_CONTEXT - 69)) | (1 << (XQueryParser.KW_COPY_NS - 69)) | (1 << (XQueryParser.KW_COUNT - 69)) | (1 << (XQueryParser.KW_DECLARE - 69)) | (1 << (XQueryParser.KW_DEFAULT - 69)) | (1 << (XQueryParser.KW_DESCENDANT - 69)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 69)) | (1 << (XQueryParser.KW_DESCENDING - 69)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 69)) | (1 << (XQueryParser.KW_DIV - 69)) | (1 << (XQueryParser.KW_DOCUMENT - 69)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 69)) | (1 << (XQueryParser.KW_ELEMENT - 69)) | (1 << (XQueryParser.KW_ELSE - 69)) | (1 << (XQueryParser.KW_EMPTY - 69)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 69)) | (1 << (XQueryParser.KW_ENCODING - 69)) | (1 << (XQueryParser.KW_END - 69)) | (1 << (XQueryParser.KW_EQ - 69)) | (1 << (XQueryParser.KW_EVERY - 69)) | (1 << (XQueryParser.KW_EXCEPT - 69)) | (1 << (XQueryParser.KW_EXTERNAL - 69)) | (1 << (XQueryParser.KW_FOLLOWING - 69)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 69)) | (1 << (XQueryParser.KW_FOR - 69)) | (1 << (XQueryParser.KW_FUNCTION - 69)) | (1 << (XQueryParser.KW_GE - 69)) | (1 << (XQueryParser.KW_GREATEST - 69)) | (1 << (XQueryParser.KW_GROUP - 69)) | (1 << (XQueryParser.KW_GT - 69)) | (1 << (XQueryParser.KW_IDIV - 69)) | (1 << (XQueryParser.KW_IF - 69)) | (1 << (XQueryParser.KW_IMPORT - 69)) | (1 << (XQueryParser.KW_IN - 69)) | (1 << (XQueryParser.KW_INHERIT - 69)) | (1 << (XQueryParser.KW_INSTANCE - 69)) | (1 << (XQueryParser.KW_INTERSECT - 69)) | (1 << (XQueryParser.KW_IS - 69)) | (1 << (XQueryParser.KW_ITEM - 69)) | (1 << (XQueryParser.KW_LAX - 69)) | (1 << (XQueryParser.KW_LE - 69)) | (1 << (XQueryParser.KW_LEAST - 69)) | (1 << (XQueryParser.KW_LET - 69)) | (1 << (XQueryParser.KW_LT - 69)) | (1 << (XQueryParser.KW_MAP - 69)) | (1 << (XQueryParser.KW_MOD - 69)) | (1 << (XQueryParser.KW_MODULE - 69)) | (1 << (XQueryParser.KW_NAMESPACE - 69)) | (1 << (XQueryParser.KW_NE - 69)) | (1 << (XQueryParser.KW_NEXT - 69)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 69)) | (1 << (XQueryParser.KW_NO_INHERIT - 69)) | (1 << (XQueryParser.KW_NO_PRESERVE - 69)) | (1 << (XQueryParser.KW_NODE - 69)) | (1 << (XQueryParser.KW_OF - 69)) | (1 << (XQueryParser.KW_ONLY - 69)) | (1 << (XQueryParser.KW_OPTION - 69)) | (1 << (XQueryParser.KW_OR - 69)) | (1 << (XQueryParser.KW_ORDER - 69)))) != 0) or ((((_la - 133)) & ~0x3f) == 0 and ((1 << (_la - 133)) & ((1 << (XQueryParser.KW_ORDERED - 133)) | (1 << (XQueryParser.KW_ORDERING - 133)) | (1 << (XQueryParser.KW_PARENT - 133)) | (1 << (XQueryParser.KW_PRECEDING - 133)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 133)) | (1 << (XQueryParser.KW_PRESERVE - 133)) | (1 << (XQueryParser.KW_PI - 133)) | (1 << (XQueryParser.KW_RETURN - 133)) | (1 << (XQueryParser.KW_SATISFIES - 133)) | (1 << (XQueryParser.KW_SCHEMA - 133)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 133)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 133)) | (1 << (XQueryParser.KW_SELF - 133)) | (1 << (XQueryParser.KW_SLIDING - 133)) | (1 << (XQueryParser.KW_SOME - 133)) | (1 << (XQueryParser.KW_STABLE - 133)) | (1 << (XQueryParser.KW_START - 133)) | (1 << (XQueryParser.KW_STRICT - 133)) | (1 << (XQueryParser.KW_STRIP - 133)) | (1 << (XQueryParser.KW_SWITCH - 133)) | (1 << (XQueryParser.KW_TEXT - 133)) | (1 << (XQueryParser.KW_THEN - 133)) | (1 << (XQueryParser.KW_TO - 133)) | (1 << (XQueryParser.KW_TREAT - 133)) | (1 << (XQueryParser.KW_TRY - 133)) | (1 << (XQueryParser.KW_TUMBLING - 133)) | (1 << (XQueryParser.KW_TYPE - 133)) | (1 << (XQueryParser.KW_TYPESWITCH - 133)) | (1 << (XQueryParser.KW_UNION - 133)) | (1 << (XQueryParser.KW_UNORDERED - 133)) | (1 << (XQueryParser.KW_UPDATE - 133)) | (1 << (XQueryParser.KW_VALIDATE - 133)) | (1 << (XQueryParser.KW_VARIABLE - 133)) | (1 << (XQueryParser.KW_VERSION - 133)) | (1 << (XQueryParser.KW_WHEN - 133)) | (1 << (XQueryParser.KW_WHERE - 133)) | (1 << (XQueryParser.KW_WINDOW - 133)) | (1 << (XQueryParser.KW_XQUERY - 133)) | (1 << (XQueryParser.KW_ARRAY_NODE - 133)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 133)) | (1 << (XQueryParser.KW_NULL_NODE - 133)) | (1 << (XQueryParser.KW_NUMBER_NODE - 133)) | (1 << (XQueryParser.KW_OBJECT_NODE - 133)) | (1 << (XQueryParser.KW_REPLACE - 133)) | (1 << (XQueryParser.KW_WITH - 133)) | (1 << (XQueryParser.KW_VALUE - 133)) | (1 << (XQueryParser.KW_INSERT - 133)) | (1 << (XQueryParser.KW_INTO - 133)) | (1 << (XQueryParser.KW_DELETE - 133)) | (1 << (XQueryParser.KW_RENAME - 133)) | (1 << (XQueryParser.URIQualifiedName - 133)) | (1 << (XQueryParser.FullQName - 133)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 133)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 133)) | (1 << (XQueryParser.NCName - 133)) | (1 << (XQueryParser.ENTER_STRING - 133)))) != 0):
                self.state = 1751
                self.exprSingle()
                self.state = 1756
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 1752
                    self.match(XQueryParser.COMMA)
                    self.state = 1753
                    self.exprSingle()
                    self.state = 1758
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 1761
            self.match(XQueryParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CurlyArrayConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ARRAY(self):
            return self.getToken(XQueryParser.KW_ARRAY, 0)

        def enclosedExpression(self):
            return self.getTypedRuleContext(XQueryParser.EnclosedExpressionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_curlyArrayConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCurlyArrayConstructor" ):
                listener.enterCurlyArrayConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCurlyArrayConstructor" ):
                listener.exitCurlyArrayConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCurlyArrayConstructor" ):
                return visitor.visitCurlyArrayConstructor(self)
            else:
                return visitor.visitChildren(self)




    def curlyArrayConstructor(self):

        localctx = XQueryParser.CurlyArrayConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 352, self.RULE_curlyArrayConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1763
            self.match(XQueryParser.KW_ARRAY)
            self.state = 1764
            self.enclosedExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringConstructorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTER_STRING(self):
            return self.getToken(XQueryParser.ENTER_STRING, 0)

        def stringConstructorContent(self):
            return self.getTypedRuleContext(XQueryParser.StringConstructorContentContext,0)


        def EXIT_STRING(self):
            return self.getToken(XQueryParser.EXIT_STRING, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_stringConstructor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringConstructor" ):
                listener.enterStringConstructor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringConstructor" ):
                listener.exitStringConstructor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringConstructor" ):
                return visitor.visitStringConstructor(self)
            else:
                return visitor.visitChildren(self)




    def stringConstructor(self):

        localctx = XQueryParser.StringConstructorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 354, self.RULE_stringConstructor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1766
            self.match(XQueryParser.ENTER_STRING)
            self.state = 1767
            self.stringConstructorContent()
            self.state = 1768
            self.match(XQueryParser.EXIT_STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringConstructorContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringConstructorChars(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringConstructorCharsContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringConstructorCharsContext,i)


        def stringConstructorInterpolation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringConstructorInterpolationContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringConstructorInterpolationContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_stringConstructorContent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringConstructorContent" ):
                listener.enterStringConstructorContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringConstructorContent" ):
                listener.exitStringConstructorContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringConstructorContent" ):
                return visitor.visitStringConstructorContent(self)
            else:
                return visitor.visitChildren(self)




    def stringConstructorContent(self):

        localctx = XQueryParser.StringConstructorContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 356, self.RULE_stringConstructorContent)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1770
            self.stringConstructorChars()
            self.state = 1776
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.ENTER_INTERPOLATION:
                self.state = 1771
                self.stringConstructorInterpolation()
                self.state = 1772
                self.stringConstructorChars()
                self.state = 1778
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharNoGraveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASIC_CHAR(self):
            return self.getToken(XQueryParser.BASIC_CHAR, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def RBRACKET(self):
            return self.getToken(XQueryParser.RBRACKET, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_charNoGrave

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharNoGrave" ):
                listener.enterCharNoGrave(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharNoGrave" ):
                listener.exitCharNoGrave(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharNoGrave" ):
                return visitor.visitCharNoGrave(self)
            else:
                return visitor.visitChildren(self)




    def charNoGrave(self):

        localctx = XQueryParser.CharNoGraveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 358, self.RULE_charNoGrave)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1779
            _la = self._input.LA(1)
            if not(_la==XQueryParser.RBRACKET or _la==XQueryParser.LBRACE or _la==XQueryParser.BASIC_CHAR):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharNoLBraceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASIC_CHAR(self):
            return self.getToken(XQueryParser.BASIC_CHAR, 0)

        def GRAVE(self):
            return self.getToken(XQueryParser.GRAVE, 0)

        def RBRACKET(self):
            return self.getToken(XQueryParser.RBRACKET, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_charNoLBrace

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharNoLBrace" ):
                listener.enterCharNoLBrace(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharNoLBrace" ):
                listener.exitCharNoLBrace(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharNoLBrace" ):
                return visitor.visitCharNoLBrace(self)
            else:
                return visitor.visitChildren(self)




    def charNoLBrace(self):

        localctx = XQueryParser.CharNoLBraceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 360, self.RULE_charNoLBrace)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1781
            _la = self._input.LA(1)
            if not(_la==XQueryParser.RBRACKET or _la==XQueryParser.GRAVE or _la==XQueryParser.BASIC_CHAR):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CharNoRBrackContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASIC_CHAR(self):
            return self.getToken(XQueryParser.BASIC_CHAR, 0)

        def GRAVE(self):
            return self.getToken(XQueryParser.GRAVE, 0)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_charNoRBrack

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCharNoRBrack" ):
                listener.enterCharNoRBrack(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCharNoRBrack" ):
                listener.exitCharNoRBrack(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCharNoRBrack" ):
                return visitor.visitCharNoRBrack(self)
            else:
                return visitor.visitChildren(self)




    def charNoRBrack(self):

        localctx = XQueryParser.CharNoRBrackContext(self, self._ctx, self.state)
        self.enterRule(localctx, 362, self.RULE_charNoRBrack)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1783
            _la = self._input.LA(1)
            if not(_la==XQueryParser.LBRACE or _la==XQueryParser.GRAVE or _la==XQueryParser.BASIC_CHAR):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringConstructorCharsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASIC_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.BASIC_CHAR)
            else:
                return self.getToken(XQueryParser.BASIC_CHAR, i)

        def charNoGrave(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.CharNoGraveContext)
            else:
                return self.getTypedRuleContext(XQueryParser.CharNoGraveContext,i)


        def charNoLBrace(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.CharNoLBraceContext)
            else:
                return self.getTypedRuleContext(XQueryParser.CharNoLBraceContext,i)


        def charNoRBrack(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.CharNoRBrackContext)
            else:
                return self.getTypedRuleContext(XQueryParser.CharNoRBrackContext,i)


        def LBRACE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.LBRACE)
            else:
                return self.getToken(XQueryParser.LBRACE, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_stringConstructorChars

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringConstructorChars" ):
                listener.enterStringConstructorChars(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringConstructorChars" ):
                listener.exitStringConstructorChars(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringConstructorChars" ):
                return visitor.visitStringConstructorChars(self)
            else:
                return visitor.visitChildren(self)




    def stringConstructorChars(self):

        localctx = XQueryParser.StringConstructorCharsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 364, self.RULE_stringConstructorChars)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1797
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.RBRACKET) | (1 << XQueryParser.LBRACE) | (1 << XQueryParser.GRAVE))) != 0) or _la==XQueryParser.BASIC_CHAR:
                self.state = 1795
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,159,self._ctx)
                if la_ == 1:
                    self.state = 1785
                    self.match(XQueryParser.BASIC_CHAR)
                    pass

                elif la_ == 2:
                    self.state = 1786
                    self.charNoGrave()
                    self.state = 1787
                    self.charNoLBrace()
                    pass

                elif la_ == 3:
                    self.state = 1789
                    self.charNoRBrack()
                    self.state = 1790
                    self.charNoGrave()
                    self.state = 1791
                    self.charNoGrave()
                    pass

                elif la_ == 4:
                    self.state = 1793
                    self.charNoGrave()
                    pass

                elif la_ == 5:
                    self.state = 1794
                    self.match(XQueryParser.LBRACE)
                    pass


                self.state = 1799
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringConstructorInterpolationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTER_INTERPOLATION(self):
            return self.getToken(XQueryParser.ENTER_INTERPOLATION, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def EXIT_INTERPOLATION(self):
            return self.getToken(XQueryParser.EXIT_INTERPOLATION, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_stringConstructorInterpolation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringConstructorInterpolation" ):
                listener.enterStringConstructorInterpolation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringConstructorInterpolation" ):
                listener.exitStringConstructorInterpolation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringConstructorInterpolation" ):
                return visitor.visitStringConstructorInterpolation(self)
            else:
                return visitor.visitChildren(self)




    def stringConstructorInterpolation(self):

        localctx = XQueryParser.StringConstructorInterpolationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 366, self.RULE_stringConstructorInterpolation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1800
            self.match(XQueryParser.ENTER_INTERPOLATION)
            self.state = 1801
            self.expr()
            self.state = 1802
            self.match(XQueryParser.EXIT_INTERPOLATION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryLookupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUESTION(self):
            return self.getToken(XQueryParser.QUESTION, 0)

        def keySpecifier(self):
            return self.getTypedRuleContext(XQueryParser.KeySpecifierContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_unaryLookup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryLookup" ):
                listener.enterUnaryLookup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryLookup" ):
                listener.exitUnaryLookup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryLookup" ):
                return visitor.visitUnaryLookup(self)
            else:
                return visitor.visitChildren(self)




    def unaryLookup(self):

        localctx = XQueryParser.UnaryLookupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 368, self.RULE_unaryLookup)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1804
            self.match(XQueryParser.QUESTION)
            self.state = 1805
            self.keySpecifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SingleTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simpleTypeName(self):
            return self.getTypedRuleContext(XQueryParser.SimpleTypeNameContext,0)


        def QUESTION(self):
            return self.getToken(XQueryParser.QUESTION, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_singleType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleType" ):
                listener.enterSingleType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleType" ):
                listener.exitSingleType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleType" ):
                return visitor.visitSingleType(self)
            else:
                return visitor.visitChildren(self)




    def singleType(self):

        localctx = XQueryParser.SingleTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 370, self.RULE_singleType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1807
            self.simpleTypeName()
            self.state = 1809
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,161,self._ctx)
            if la_ == 1:
                self.state = 1808
                self.match(XQueryParser.QUESTION)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_typeDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeDeclaration" ):
                listener.enterTypeDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeDeclaration" ):
                listener.exitTypeDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeDeclaration" ):
                return visitor.visitTypeDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def typeDeclaration(self):

        localctx = XQueryParser.TypeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 372, self.RULE_typeDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1811
            self.match(XQueryParser.KW_AS)
            self.state = 1812
            self.sequenceType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SequenceTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.occurrence = None # Token

        def KW_EMPTY_SEQUENCE(self):
            return self.getToken(XQueryParser.KW_EMPTY_SEQUENCE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def itemType(self):
            return self.getTypedRuleContext(XQueryParser.ItemTypeContext,0)


        def QUESTION(self):
            return self.getToken(XQueryParser.QUESTION, 0)

        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def PLUS(self):
            return self.getToken(XQueryParser.PLUS, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_sequenceType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSequenceType" ):
                listener.enterSequenceType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSequenceType" ):
                listener.exitSequenceType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSequenceType" ):
                return visitor.visitSequenceType(self)
            else:
                return visitor.visitChildren(self)




    def sequenceType(self):

        localctx = XQueryParser.SequenceTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 374, self.RULE_sequenceType)
        self._la = 0 # Token type
        try:
            self.state = 1821
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,163,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1814
                self.match(XQueryParser.KW_EMPTY_SEQUENCE)
                self.state = 1815
                self.match(XQueryParser.LPAREN)
                self.state = 1816
                self.match(XQueryParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1817
                self.itemType()
                self.state = 1819
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,162,self._ctx)
                if la_ == 1:
                    self.state = 1818
                    localctx.occurrence = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.STAR) | (1 << XQueryParser.PLUS) | (1 << XQueryParser.QUESTION))) != 0)):
                        localctx.occurrence = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ItemTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def kindTest(self):
            return self.getTypedRuleContext(XQueryParser.KindTestContext,0)


        def KW_ITEM(self):
            return self.getToken(XQueryParser.KW_ITEM, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def functionTest(self):
            return self.getTypedRuleContext(XQueryParser.FunctionTestContext,0)


        def mapTest(self):
            return self.getTypedRuleContext(XQueryParser.MapTestContext,0)


        def arrayTest(self):
            return self.getTypedRuleContext(XQueryParser.ArrayTestContext,0)


        def atomicOrUnionType(self):
            return self.getTypedRuleContext(XQueryParser.AtomicOrUnionTypeContext,0)


        def parenthesizedItemTest(self):
            return self.getTypedRuleContext(XQueryParser.ParenthesizedItemTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_itemType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterItemType" ):
                listener.enterItemType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitItemType" ):
                listener.exitItemType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitItemType" ):
                return visitor.visitItemType(self)
            else:
                return visitor.visitChildren(self)




    def itemType(self):

        localctx = XQueryParser.ItemTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 376, self.RULE_itemType)
        try:
            self.state = 1832
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,164,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1823
                self.kindTest()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1824
                self.match(XQueryParser.KW_ITEM)
                self.state = 1825
                self.match(XQueryParser.LPAREN)
                self.state = 1826
                self.match(XQueryParser.RPAREN)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1827
                self.functionTest()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1828
                self.mapTest()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1829
                self.arrayTest()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1830
                self.atomicOrUnionType()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1831
                self.parenthesizedItemTest()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomicOrUnionTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_atomicOrUnionType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomicOrUnionType" ):
                listener.enterAtomicOrUnionType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomicOrUnionType" ):
                listener.exitAtomicOrUnionType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomicOrUnionType" ):
                return visitor.visitAtomicOrUnionType(self)
            else:
                return visitor.visitChildren(self)




    def atomicOrUnionType(self):

        localctx = XQueryParser.AtomicOrUnionTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 378, self.RULE_atomicOrUnionType)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1834
            self.eqName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KindTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def documentTest(self):
            return self.getTypedRuleContext(XQueryParser.DocumentTestContext,0)


        def elementTest(self):
            return self.getTypedRuleContext(XQueryParser.ElementTestContext,0)


        def attributeTest(self):
            return self.getTypedRuleContext(XQueryParser.AttributeTestContext,0)


        def schemaElementTest(self):
            return self.getTypedRuleContext(XQueryParser.SchemaElementTestContext,0)


        def schemaAttributeTest(self):
            return self.getTypedRuleContext(XQueryParser.SchemaAttributeTestContext,0)


        def piTest(self):
            return self.getTypedRuleContext(XQueryParser.PiTestContext,0)


        def commentTest(self):
            return self.getTypedRuleContext(XQueryParser.CommentTestContext,0)


        def textTest(self):
            return self.getTypedRuleContext(XQueryParser.TextTestContext,0)


        def namespaceNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.NamespaceNodeTestContext,0)


        def mlNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.MlNodeTestContext,0)


        def binaryNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.BinaryNodeTestContext,0)


        def anyKindTest(self):
            return self.getTypedRuleContext(XQueryParser.AnyKindTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_kindTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKindTest" ):
                listener.enterKindTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKindTest" ):
                listener.exitKindTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKindTest" ):
                return visitor.visitKindTest(self)
            else:
                return visitor.visitChildren(self)




    def kindTest(self):

        localctx = XQueryParser.KindTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 380, self.RULE_kindTest)
        try:
            self.state = 1848
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_DOCUMENT_NODE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1836
                self.documentTest()
                pass
            elif token in [XQueryParser.KW_ELEMENT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1837
                self.elementTest()
                pass
            elif token in [XQueryParser.KW_ATTRIBUTE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 1838
                self.attributeTest()
                pass
            elif token in [XQueryParser.KW_SCHEMA_ELEM]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1839
                self.schemaElementTest()
                pass
            elif token in [XQueryParser.KW_SCHEMA_ATTR]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1840
                self.schemaAttributeTest()
                pass
            elif token in [XQueryParser.KW_PI]:
                self.enterOuterAlt(localctx, 6)
                self.state = 1841
                self.piTest()
                pass
            elif token in [XQueryParser.KW_COMMENT]:
                self.enterOuterAlt(localctx, 7)
                self.state = 1842
                self.commentTest()
                pass
            elif token in [XQueryParser.KW_TEXT]:
                self.enterOuterAlt(localctx, 8)
                self.state = 1843
                self.textTest()
                pass
            elif token in [XQueryParser.KW_NAMESPACE_NODE]:
                self.enterOuterAlt(localctx, 9)
                self.state = 1844
                self.namespaceNodeTest()
                pass
            elif token in [XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE]:
                self.enterOuterAlt(localctx, 10)
                self.state = 1845
                self.mlNodeTest()
                pass
            elif token in [XQueryParser.KW_BINARY]:
                self.enterOuterAlt(localctx, 11)
                self.state = 1846
                self.binaryNodeTest()
                pass
            elif token in [XQueryParser.KW_NODE]:
                self.enterOuterAlt(localctx, 12)
                self.state = 1847
                self.anyKindTest()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnyKindTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NODE(self):
            return self.getToken(XQueryParser.KW_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_anyKindTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnyKindTest" ):
                listener.enterAnyKindTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnyKindTest" ):
                listener.exitAnyKindTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnyKindTest" ):
                return visitor.visitAnyKindTest(self)
            else:
                return visitor.visitChildren(self)




    def anyKindTest(self):

        localctx = XQueryParser.AnyKindTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 382, self.RULE_anyKindTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1850
            self.match(XQueryParser.KW_NODE)
            self.state = 1851
            self.match(XQueryParser.LPAREN)
            self.state = 1853
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.STAR:
                self.state = 1852
                self.match(XQueryParser.STAR)


            self.state = 1855
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BinaryNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_BINARY(self):
            return self.getToken(XQueryParser.KW_BINARY, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_binaryNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinaryNodeTest" ):
                listener.enterBinaryNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinaryNodeTest" ):
                listener.exitBinaryNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinaryNodeTest" ):
                return visitor.visitBinaryNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def binaryNodeTest(self):

        localctx = XQueryParser.BinaryNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 384, self.RULE_binaryNodeTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1857
            self.match(XQueryParser.KW_BINARY)
            self.state = 1858
            self.match(XQueryParser.LPAREN)
            self.state = 1859
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DocumentTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_DOCUMENT_NODE(self):
            return self.getToken(XQueryParser.KW_DOCUMENT_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def elementTest(self):
            return self.getTypedRuleContext(XQueryParser.ElementTestContext,0)


        def schemaElementTest(self):
            return self.getTypedRuleContext(XQueryParser.SchemaElementTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_documentTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocumentTest" ):
                listener.enterDocumentTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocumentTest" ):
                listener.exitDocumentTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDocumentTest" ):
                return visitor.visitDocumentTest(self)
            else:
                return visitor.visitChildren(self)




    def documentTest(self):

        localctx = XQueryParser.DocumentTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 386, self.RULE_documentTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1861
            self.match(XQueryParser.KW_DOCUMENT_NODE)
            self.state = 1862
            self.match(XQueryParser.LPAREN)
            self.state = 1865
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_ELEMENT]:
                self.state = 1863
                self.elementTest()
                pass
            elif token in [XQueryParser.KW_SCHEMA_ELEM]:
                self.state = 1864
                self.schemaElementTest()
                pass
            elif token in [XQueryParser.RPAREN]:
                pass
            else:
                pass
            self.state = 1867
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TextTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_TEXT(self):
            return self.getToken(XQueryParser.KW_TEXT, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_textTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTextTest" ):
                listener.enterTextTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTextTest" ):
                listener.exitTextTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTextTest" ):
                return visitor.visitTextTest(self)
            else:
                return visitor.visitChildren(self)




    def textTest(self):

        localctx = XQueryParser.TextTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 388, self.RULE_textTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1869
            self.match(XQueryParser.KW_TEXT)
            self.state = 1870
            self.match(XQueryParser.LPAREN)
            self.state = 1871
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommentTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_COMMENT(self):
            return self.getToken(XQueryParser.KW_COMMENT, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_commentTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommentTest" ):
                listener.enterCommentTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommentTest" ):
                listener.exitCommentTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommentTest" ):
                return visitor.visitCommentTest(self)
            else:
                return visitor.visitChildren(self)




    def commentTest(self):

        localctx = XQueryParser.CommentTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 390, self.RULE_commentTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1873
            self.match(XQueryParser.KW_COMMENT)
            self.state = 1874
            self.match(XQueryParser.LPAREN)
            self.state = 1875
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamespaceNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NAMESPACE_NODE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_namespaceNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamespaceNodeTest" ):
                listener.enterNamespaceNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamespaceNodeTest" ):
                listener.exitNamespaceNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamespaceNodeTest" ):
                return visitor.visitNamespaceNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def namespaceNodeTest(self):

        localctx = XQueryParser.NamespaceNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 392, self.RULE_namespaceNodeTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1877
            self.match(XQueryParser.KW_NAMESPACE_NODE)
            self.state = 1878
            self.match(XQueryParser.LPAREN)
            self.state = 1879
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PiTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_PI(self):
            return self.getToken(XQueryParser.KW_PI, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_piTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPiTest" ):
                listener.enterPiTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPiTest" ):
                listener.exitPiTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPiTest" ):
                return visitor.visitPiTest(self)
            else:
                return visitor.visitChildren(self)




    def piTest(self):

        localctx = XQueryParser.PiTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 394, self.RULE_piTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1881
            self.match(XQueryParser.KW_PI)
            self.state = 1882
            self.match(XQueryParser.LPAREN)
            self.state = 1885
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.NCName]:
                self.state = 1883
                self.ncName()
                pass
            elif token in [XQueryParser.Quot, XQueryParser.Apos]:
                self.state = 1884
                self.stringLiteral()
                pass
            elif token in [XQueryParser.RPAREN]:
                pass
            else:
                pass
            self.state = 1887
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ATTRIBUTE(self):
            return self.getToken(XQueryParser.KW_ATTRIBUTE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def attributeNameOrWildcard(self):
            return self.getTypedRuleContext(XQueryParser.AttributeNameOrWildcardContext,0)


        def COMMA(self):
            return self.getToken(XQueryParser.COMMA, 0)

        def typeName(self):
            return self.getTypedRuleContext(XQueryParser.TypeNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_attributeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeTest" ):
                listener.enterAttributeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeTest" ):
                listener.exitAttributeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeTest" ):
                return visitor.visitAttributeTest(self)
            else:
                return visitor.visitChildren(self)




    def attributeTest(self):

        localctx = XQueryParser.AttributeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 396, self.RULE_attributeTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1889
            self.match(XQueryParser.KW_ATTRIBUTE)
            self.state = 1890
            self.match(XQueryParser.LPAREN)
            self.state = 1896
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.STAR) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ANCESTOR) | (1 << XQueryParser.KW_ANCESTOR_OR_SELF) | (1 << XQueryParser.KW_AND) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_AS) | (1 << XQueryParser.KW_ASCENDING) | (1 << XQueryParser.KW_AT) | (1 << XQueryParser.KW_ATTRIBUTE) | (1 << XQueryParser.KW_BASE_URI) | (1 << XQueryParser.KW_BOUNDARY_SPACE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_BY - 64)) | (1 << (XQueryParser.KW_CASE - 64)) | (1 << (XQueryParser.KW_CAST - 64)) | (1 << (XQueryParser.KW_CASTABLE - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_CHILD - 64)) | (1 << (XQueryParser.KW_COLLATION - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONSTRUCTION - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COPY_NS - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECLARE - 64)) | (1 << (XQueryParser.KW_DEFAULT - 64)) | (1 << (XQueryParser.KW_DESCENDANT - 64)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 64)) | (1 << (XQueryParser.KW_DESCENDING - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DIV - 64)) | (1 << (XQueryParser.KW_DOCUMENT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_ELSE - 64)) | (1 << (XQueryParser.KW_EMPTY - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_ENCODING - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_EQ - 64)) | (1 << (XQueryParser.KW_EVERY - 64)) | (1 << (XQueryParser.KW_EXCEPT - 64)) | (1 << (XQueryParser.KW_EXTERNAL - 64)) | (1 << (XQueryParser.KW_FOLLOWING - 64)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 64)) | (1 << (XQueryParser.KW_FOR - 64)) | (1 << (XQueryParser.KW_FUNCTION - 64)) | (1 << (XQueryParser.KW_GE - 64)) | (1 << (XQueryParser.KW_GREATEST - 64)) | (1 << (XQueryParser.KW_GROUP - 64)) | (1 << (XQueryParser.KW_GT - 64)) | (1 << (XQueryParser.KW_IDIV - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_IMPORT - 64)) | (1 << (XQueryParser.KW_IN - 64)) | (1 << (XQueryParser.KW_INHERIT - 64)) | (1 << (XQueryParser.KW_INSTANCE - 64)) | (1 << (XQueryParser.KW_INTERSECT - 64)) | (1 << (XQueryParser.KW_IS - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_LAX - 64)) | (1 << (XQueryParser.KW_LE - 64)) | (1 << (XQueryParser.KW_LEAST - 64)) | (1 << (XQueryParser.KW_LET - 64)) | (1 << (XQueryParser.KW_LT - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_MOD - 64)) | (1 << (XQueryParser.KW_MODULE - 64)) | (1 << (XQueryParser.KW_NAMESPACE - 64)) | (1 << (XQueryParser.KW_NE - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NO_INHERIT - 64)) | (1 << (XQueryParser.KW_NO_PRESERVE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (XQueryParser.KW_OF - 128)) | (1 << (XQueryParser.KW_ONLY - 128)) | (1 << (XQueryParser.KW_OPTION - 128)) | (1 << (XQueryParser.KW_OR - 128)) | (1 << (XQueryParser.KW_ORDER - 128)) | (1 << (XQueryParser.KW_ORDERED - 128)) | (1 << (XQueryParser.KW_ORDERING - 128)) | (1 << (XQueryParser.KW_PARENT - 128)) | (1 << (XQueryParser.KW_PRECEDING - 128)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 128)) | (1 << (XQueryParser.KW_PRESERVE - 128)) | (1 << (XQueryParser.KW_PI - 128)) | (1 << (XQueryParser.KW_RETURN - 128)) | (1 << (XQueryParser.KW_SATISFIES - 128)) | (1 << (XQueryParser.KW_SCHEMA - 128)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 128)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 128)) | (1 << (XQueryParser.KW_SELF - 128)) | (1 << (XQueryParser.KW_SLIDING - 128)) | (1 << (XQueryParser.KW_SOME - 128)) | (1 << (XQueryParser.KW_STABLE - 128)) | (1 << (XQueryParser.KW_START - 128)) | (1 << (XQueryParser.KW_STRICT - 128)) | (1 << (XQueryParser.KW_STRIP - 128)) | (1 << (XQueryParser.KW_SWITCH - 128)) | (1 << (XQueryParser.KW_TEXT - 128)) | (1 << (XQueryParser.KW_THEN - 128)) | (1 << (XQueryParser.KW_TO - 128)) | (1 << (XQueryParser.KW_TREAT - 128)) | (1 << (XQueryParser.KW_TRY - 128)) | (1 << (XQueryParser.KW_TUMBLING - 128)) | (1 << (XQueryParser.KW_TYPE - 128)) | (1 << (XQueryParser.KW_TYPESWITCH - 128)) | (1 << (XQueryParser.KW_UNION - 128)) | (1 << (XQueryParser.KW_UNORDERED - 128)) | (1 << (XQueryParser.KW_UPDATE - 128)) | (1 << (XQueryParser.KW_VALIDATE - 128)) | (1 << (XQueryParser.KW_VARIABLE - 128)) | (1 << (XQueryParser.KW_VERSION - 128)) | (1 << (XQueryParser.KW_WHEN - 128)) | (1 << (XQueryParser.KW_WHERE - 128)) | (1 << (XQueryParser.KW_WINDOW - 128)) | (1 << (XQueryParser.KW_XQUERY - 128)) | (1 << (XQueryParser.KW_ARRAY_NODE - 128)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 128)) | (1 << (XQueryParser.KW_NULL_NODE - 128)) | (1 << (XQueryParser.KW_NUMBER_NODE - 128)) | (1 << (XQueryParser.KW_OBJECT_NODE - 128)) | (1 << (XQueryParser.KW_REPLACE - 128)) | (1 << (XQueryParser.KW_WITH - 128)) | (1 << (XQueryParser.KW_VALUE - 128)) | (1 << (XQueryParser.KW_INSERT - 128)) | (1 << (XQueryParser.KW_INTO - 128)) | (1 << (XQueryParser.KW_DELETE - 128)) | (1 << (XQueryParser.KW_RENAME - 128)) | (1 << (XQueryParser.URIQualifiedName - 128)) | (1 << (XQueryParser.FullQName - 128)) | (1 << (XQueryParser.NCName - 128)))) != 0):
                self.state = 1891
                self.attributeNameOrWildcard()
                self.state = 1894
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==XQueryParser.COMMA:
                    self.state = 1892
                    self.match(XQueryParser.COMMA)
                    self.state = 1893
                    self.typeName()




            self.state = 1898
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeNameOrWildcardContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def attributeName(self):
            return self.getTypedRuleContext(XQueryParser.AttributeNameContext,0)


        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_attributeNameOrWildcard

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeNameOrWildcard" ):
                listener.enterAttributeNameOrWildcard(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeNameOrWildcard" ):
                listener.exitAttributeNameOrWildcard(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeNameOrWildcard" ):
                return visitor.visitAttributeNameOrWildcard(self)
            else:
                return visitor.visitChildren(self)




    def attributeNameOrWildcard(self):

        localctx = XQueryParser.AttributeNameOrWildcardContext(self, self._ctx, self.state)
        self.enterRule(localctx, 398, self.RULE_attributeNameOrWildcard)
        try:
            self.state = 1902
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1900
                self.attributeName()
                pass
            elif token in [XQueryParser.STAR]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1901
                self.match(XQueryParser.STAR)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SchemaAttributeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_SCHEMA_ATTR(self):
            return self.getToken(XQueryParser.KW_SCHEMA_ATTR, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def attributeDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.AttributeDeclarationContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_schemaAttributeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSchemaAttributeTest" ):
                listener.enterSchemaAttributeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSchemaAttributeTest" ):
                listener.exitSchemaAttributeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSchemaAttributeTest" ):
                return visitor.visitSchemaAttributeTest(self)
            else:
                return visitor.visitChildren(self)




    def schemaAttributeTest(self):

        localctx = XQueryParser.SchemaAttributeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 400, self.RULE_schemaAttributeTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1904
            self.match(XQueryParser.KW_SCHEMA_ATTR)
            self.state = 1905
            self.match(XQueryParser.LPAREN)
            self.state = 1906
            self.attributeDeclaration()
            self.state = 1907
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.optional = None # Token

        def KW_ELEMENT(self):
            return self.getToken(XQueryParser.KW_ELEMENT, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def elementNameOrWildcard(self):
            return self.getTypedRuleContext(XQueryParser.ElementNameOrWildcardContext,0)


        def COMMA(self):
            return self.getToken(XQueryParser.COMMA, 0)

        def typeName(self):
            return self.getTypedRuleContext(XQueryParser.TypeNameContext,0)


        def QUESTION(self):
            return self.getToken(XQueryParser.QUESTION, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_elementTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementTest" ):
                listener.enterElementTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementTest" ):
                listener.exitElementTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementTest" ):
                return visitor.visitElementTest(self)
            else:
                return visitor.visitChildren(self)




    def elementTest(self):

        localctx = XQueryParser.ElementTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 402, self.RULE_elementTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1909
            self.match(XQueryParser.KW_ELEMENT)
            self.state = 1910
            self.match(XQueryParser.LPAREN)
            self.state = 1919
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.STAR) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ANCESTOR) | (1 << XQueryParser.KW_ANCESTOR_OR_SELF) | (1 << XQueryParser.KW_AND) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_AS) | (1 << XQueryParser.KW_ASCENDING) | (1 << XQueryParser.KW_AT) | (1 << XQueryParser.KW_ATTRIBUTE) | (1 << XQueryParser.KW_BASE_URI) | (1 << XQueryParser.KW_BOUNDARY_SPACE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_BY - 64)) | (1 << (XQueryParser.KW_CASE - 64)) | (1 << (XQueryParser.KW_CAST - 64)) | (1 << (XQueryParser.KW_CASTABLE - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_CHILD - 64)) | (1 << (XQueryParser.KW_COLLATION - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONSTRUCTION - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COPY_NS - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECLARE - 64)) | (1 << (XQueryParser.KW_DEFAULT - 64)) | (1 << (XQueryParser.KW_DESCENDANT - 64)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 64)) | (1 << (XQueryParser.KW_DESCENDING - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DIV - 64)) | (1 << (XQueryParser.KW_DOCUMENT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_ELSE - 64)) | (1 << (XQueryParser.KW_EMPTY - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_ENCODING - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_EQ - 64)) | (1 << (XQueryParser.KW_EVERY - 64)) | (1 << (XQueryParser.KW_EXCEPT - 64)) | (1 << (XQueryParser.KW_EXTERNAL - 64)) | (1 << (XQueryParser.KW_FOLLOWING - 64)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 64)) | (1 << (XQueryParser.KW_FOR - 64)) | (1 << (XQueryParser.KW_FUNCTION - 64)) | (1 << (XQueryParser.KW_GE - 64)) | (1 << (XQueryParser.KW_GREATEST - 64)) | (1 << (XQueryParser.KW_GROUP - 64)) | (1 << (XQueryParser.KW_GT - 64)) | (1 << (XQueryParser.KW_IDIV - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_IMPORT - 64)) | (1 << (XQueryParser.KW_IN - 64)) | (1 << (XQueryParser.KW_INHERIT - 64)) | (1 << (XQueryParser.KW_INSTANCE - 64)) | (1 << (XQueryParser.KW_INTERSECT - 64)) | (1 << (XQueryParser.KW_IS - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_LAX - 64)) | (1 << (XQueryParser.KW_LE - 64)) | (1 << (XQueryParser.KW_LEAST - 64)) | (1 << (XQueryParser.KW_LET - 64)) | (1 << (XQueryParser.KW_LT - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_MOD - 64)) | (1 << (XQueryParser.KW_MODULE - 64)) | (1 << (XQueryParser.KW_NAMESPACE - 64)) | (1 << (XQueryParser.KW_NE - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NO_INHERIT - 64)) | (1 << (XQueryParser.KW_NO_PRESERVE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (XQueryParser.KW_OF - 128)) | (1 << (XQueryParser.KW_ONLY - 128)) | (1 << (XQueryParser.KW_OPTION - 128)) | (1 << (XQueryParser.KW_OR - 128)) | (1 << (XQueryParser.KW_ORDER - 128)) | (1 << (XQueryParser.KW_ORDERED - 128)) | (1 << (XQueryParser.KW_ORDERING - 128)) | (1 << (XQueryParser.KW_PARENT - 128)) | (1 << (XQueryParser.KW_PRECEDING - 128)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 128)) | (1 << (XQueryParser.KW_PRESERVE - 128)) | (1 << (XQueryParser.KW_PI - 128)) | (1 << (XQueryParser.KW_RETURN - 128)) | (1 << (XQueryParser.KW_SATISFIES - 128)) | (1 << (XQueryParser.KW_SCHEMA - 128)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 128)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 128)) | (1 << (XQueryParser.KW_SELF - 128)) | (1 << (XQueryParser.KW_SLIDING - 128)) | (1 << (XQueryParser.KW_SOME - 128)) | (1 << (XQueryParser.KW_STABLE - 128)) | (1 << (XQueryParser.KW_START - 128)) | (1 << (XQueryParser.KW_STRICT - 128)) | (1 << (XQueryParser.KW_STRIP - 128)) | (1 << (XQueryParser.KW_SWITCH - 128)) | (1 << (XQueryParser.KW_TEXT - 128)) | (1 << (XQueryParser.KW_THEN - 128)) | (1 << (XQueryParser.KW_TO - 128)) | (1 << (XQueryParser.KW_TREAT - 128)) | (1 << (XQueryParser.KW_TRY - 128)) | (1 << (XQueryParser.KW_TUMBLING - 128)) | (1 << (XQueryParser.KW_TYPE - 128)) | (1 << (XQueryParser.KW_TYPESWITCH - 128)) | (1 << (XQueryParser.KW_UNION - 128)) | (1 << (XQueryParser.KW_UNORDERED - 128)) | (1 << (XQueryParser.KW_UPDATE - 128)) | (1 << (XQueryParser.KW_VALIDATE - 128)) | (1 << (XQueryParser.KW_VARIABLE - 128)) | (1 << (XQueryParser.KW_VERSION - 128)) | (1 << (XQueryParser.KW_WHEN - 128)) | (1 << (XQueryParser.KW_WHERE - 128)) | (1 << (XQueryParser.KW_WINDOW - 128)) | (1 << (XQueryParser.KW_XQUERY - 128)) | (1 << (XQueryParser.KW_ARRAY_NODE - 128)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 128)) | (1 << (XQueryParser.KW_NULL_NODE - 128)) | (1 << (XQueryParser.KW_NUMBER_NODE - 128)) | (1 << (XQueryParser.KW_OBJECT_NODE - 128)) | (1 << (XQueryParser.KW_REPLACE - 128)) | (1 << (XQueryParser.KW_WITH - 128)) | (1 << (XQueryParser.KW_VALUE - 128)) | (1 << (XQueryParser.KW_INSERT - 128)) | (1 << (XQueryParser.KW_INTO - 128)) | (1 << (XQueryParser.KW_DELETE - 128)) | (1 << (XQueryParser.KW_RENAME - 128)) | (1 << (XQueryParser.URIQualifiedName - 128)) | (1 << (XQueryParser.FullQName - 128)) | (1 << (XQueryParser.NCName - 128)))) != 0):
                self.state = 1911
                self.elementNameOrWildcard()
                self.state = 1917
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==XQueryParser.COMMA:
                    self.state = 1912
                    self.match(XQueryParser.COMMA)
                    self.state = 1913
                    self.typeName()
                    self.state = 1915
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==XQueryParser.QUESTION:
                        self.state = 1914
                        localctx.optional = self.match(XQueryParser.QUESTION)






            self.state = 1921
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementNameOrWildcardContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def elementName(self):
            return self.getTypedRuleContext(XQueryParser.ElementNameContext,0)


        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_elementNameOrWildcard

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementNameOrWildcard" ):
                listener.enterElementNameOrWildcard(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementNameOrWildcard" ):
                listener.exitElementNameOrWildcard(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementNameOrWildcard" ):
                return visitor.visitElementNameOrWildcard(self)
            else:
                return visitor.visitChildren(self)




    def elementNameOrWildcard(self):

        localctx = XQueryParser.ElementNameOrWildcardContext(self, self._ctx, self.state)
        self.enterRule(localctx, 404, self.RULE_elementNameOrWildcard)
        try:
            self.state = 1925
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1923
                self.elementName()
                pass
            elif token in [XQueryParser.STAR]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1924
                self.match(XQueryParser.STAR)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SchemaElementTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_SCHEMA_ELEM(self):
            return self.getToken(XQueryParser.KW_SCHEMA_ELEM, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def elementDeclaration(self):
            return self.getTypedRuleContext(XQueryParser.ElementDeclarationContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_schemaElementTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSchemaElementTest" ):
                listener.enterSchemaElementTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSchemaElementTest" ):
                listener.exitSchemaElementTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSchemaElementTest" ):
                return visitor.visitSchemaElementTest(self)
            else:
                return visitor.visitChildren(self)




    def schemaElementTest(self):

        localctx = XQueryParser.SchemaElementTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 406, self.RULE_schemaElementTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1927
            self.match(XQueryParser.KW_SCHEMA_ELEM)
            self.state = 1928
            self.match(XQueryParser.LPAREN)
            self.state = 1929
            self.elementDeclaration()
            self.state = 1930
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def elementName(self):
            return self.getTypedRuleContext(XQueryParser.ElementNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_elementDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementDeclaration" ):
                listener.enterElementDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementDeclaration" ):
                listener.exitElementDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementDeclaration" ):
                return visitor.visitElementDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def elementDeclaration(self):

        localctx = XQueryParser.ElementDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 408, self.RULE_elementDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1932
            self.elementName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_attributeName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeName" ):
                listener.enterAttributeName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeName" ):
                listener.exitAttributeName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeName" ):
                return visitor.visitAttributeName(self)
            else:
                return visitor.visitChildren(self)




    def attributeName(self):

        localctx = XQueryParser.AttributeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 410, self.RULE_attributeName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1934
            self.eqName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_elementName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElementName" ):
                listener.enterElementName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElementName" ):
                listener.exitElementName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElementName" ):
                return visitor.visitElementName(self)
            else:
                return visitor.visitChildren(self)




    def elementName(self):

        localctx = XQueryParser.ElementNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 412, self.RULE_elementName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1936
            self.eqName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleTypeNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeName(self):
            return self.getTypedRuleContext(XQueryParser.TypeNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_simpleTypeName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleTypeName" ):
                listener.enterSimpleTypeName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleTypeName" ):
                listener.exitSimpleTypeName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleTypeName" ):
                return visitor.visitSimpleTypeName(self)
            else:
                return visitor.visitChildren(self)




    def simpleTypeName(self):

        localctx = XQueryParser.SimpleTypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 414, self.RULE_simpleTypeName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1938
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_typeName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeName" ):
                listener.enterTypeName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeName" ):
                listener.exitTypeName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeName" ):
                return visitor.visitTypeName(self)
            else:
                return visitor.visitChildren(self)




    def typeName(self):

        localctx = XQueryParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 416, self.RULE_typeName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1940
            self.eqName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def anyFunctionTest(self):
            return self.getTypedRuleContext(XQueryParser.AnyFunctionTestContext,0)


        def typedFunctionTest(self):
            return self.getTypedRuleContext(XQueryParser.TypedFunctionTestContext,0)


        def annotation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(XQueryParser.AnnotationContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionTest" ):
                listener.enterFunctionTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionTest" ):
                listener.exitFunctionTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionTest" ):
                return visitor.visitFunctionTest(self)
            else:
                return visitor.visitChildren(self)




    def functionTest(self):

        localctx = XQueryParser.FunctionTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 418, self.RULE_functionTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1945
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==XQueryParser.MOD:
                self.state = 1942
                self.annotation()
                self.state = 1947
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1950
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,177,self._ctx)
            if la_ == 1:
                self.state = 1948
                self.anyFunctionTest()
                pass

            elif la_ == 2:
                self.state = 1949
                self.typedFunctionTest()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnyFunctionTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FUNCTION(self):
            return self.getToken(XQueryParser.KW_FUNCTION, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_anyFunctionTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnyFunctionTest" ):
                listener.enterAnyFunctionTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnyFunctionTest" ):
                listener.exitAnyFunctionTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnyFunctionTest" ):
                return visitor.visitAnyFunctionTest(self)
            else:
                return visitor.visitChildren(self)




    def anyFunctionTest(self):

        localctx = XQueryParser.AnyFunctionTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 420, self.RULE_anyFunctionTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1952
            self.match(XQueryParser.KW_FUNCTION)
            self.state = 1953
            self.match(XQueryParser.LPAREN)
            self.state = 1954
            self.match(XQueryParser.STAR)
            self.state = 1955
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypedFunctionTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_FUNCTION(self):
            return self.getToken(XQueryParser.KW_FUNCTION, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def sequenceType(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.SequenceTypeContext)
            else:
                return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_typedFunctionTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypedFunctionTest" ):
                listener.enterTypedFunctionTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypedFunctionTest" ):
                listener.exitTypedFunctionTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypedFunctionTest" ):
                return visitor.visitTypedFunctionTest(self)
            else:
                return visitor.visitChildren(self)




    def typedFunctionTest(self):

        localctx = XQueryParser.TypedFunctionTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 422, self.RULE_typedFunctionTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1957
            self.match(XQueryParser.KW_FUNCTION)
            self.state = 1958
            self.match(XQueryParser.LPAREN)
            self.state = 1967
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.LPAREN) | (1 << XQueryParser.MOD) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ANCESTOR) | (1 << XQueryParser.KW_ANCESTOR_OR_SELF) | (1 << XQueryParser.KW_AND) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_AS) | (1 << XQueryParser.KW_ASCENDING) | (1 << XQueryParser.KW_AT) | (1 << XQueryParser.KW_ATTRIBUTE) | (1 << XQueryParser.KW_BASE_URI) | (1 << XQueryParser.KW_BOUNDARY_SPACE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_BY - 64)) | (1 << (XQueryParser.KW_CASE - 64)) | (1 << (XQueryParser.KW_CAST - 64)) | (1 << (XQueryParser.KW_CASTABLE - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_CHILD - 64)) | (1 << (XQueryParser.KW_COLLATION - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONSTRUCTION - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COPY_NS - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECLARE - 64)) | (1 << (XQueryParser.KW_DEFAULT - 64)) | (1 << (XQueryParser.KW_DESCENDANT - 64)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 64)) | (1 << (XQueryParser.KW_DESCENDING - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DIV - 64)) | (1 << (XQueryParser.KW_DOCUMENT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_ELSE - 64)) | (1 << (XQueryParser.KW_EMPTY - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_ENCODING - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_EQ - 64)) | (1 << (XQueryParser.KW_EVERY - 64)) | (1 << (XQueryParser.KW_EXCEPT - 64)) | (1 << (XQueryParser.KW_EXTERNAL - 64)) | (1 << (XQueryParser.KW_FOLLOWING - 64)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 64)) | (1 << (XQueryParser.KW_FOR - 64)) | (1 << (XQueryParser.KW_FUNCTION - 64)) | (1 << (XQueryParser.KW_GE - 64)) | (1 << (XQueryParser.KW_GREATEST - 64)) | (1 << (XQueryParser.KW_GROUP - 64)) | (1 << (XQueryParser.KW_GT - 64)) | (1 << (XQueryParser.KW_IDIV - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_IMPORT - 64)) | (1 << (XQueryParser.KW_IN - 64)) | (1 << (XQueryParser.KW_INHERIT - 64)) | (1 << (XQueryParser.KW_INSTANCE - 64)) | (1 << (XQueryParser.KW_INTERSECT - 64)) | (1 << (XQueryParser.KW_IS - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_LAX - 64)) | (1 << (XQueryParser.KW_LE - 64)) | (1 << (XQueryParser.KW_LEAST - 64)) | (1 << (XQueryParser.KW_LET - 64)) | (1 << (XQueryParser.KW_LT - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_MOD - 64)) | (1 << (XQueryParser.KW_MODULE - 64)) | (1 << (XQueryParser.KW_NAMESPACE - 64)) | (1 << (XQueryParser.KW_NE - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NO_INHERIT - 64)) | (1 << (XQueryParser.KW_NO_PRESERVE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (XQueryParser.KW_OF - 128)) | (1 << (XQueryParser.KW_ONLY - 128)) | (1 << (XQueryParser.KW_OPTION - 128)) | (1 << (XQueryParser.KW_OR - 128)) | (1 << (XQueryParser.KW_ORDER - 128)) | (1 << (XQueryParser.KW_ORDERED - 128)) | (1 << (XQueryParser.KW_ORDERING - 128)) | (1 << (XQueryParser.KW_PARENT - 128)) | (1 << (XQueryParser.KW_PRECEDING - 128)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 128)) | (1 << (XQueryParser.KW_PRESERVE - 128)) | (1 << (XQueryParser.KW_PI - 128)) | (1 << (XQueryParser.KW_RETURN - 128)) | (1 << (XQueryParser.KW_SATISFIES - 128)) | (1 << (XQueryParser.KW_SCHEMA - 128)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 128)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 128)) | (1 << (XQueryParser.KW_SELF - 128)) | (1 << (XQueryParser.KW_SLIDING - 128)) | (1 << (XQueryParser.KW_SOME - 128)) | (1 << (XQueryParser.KW_STABLE - 128)) | (1 << (XQueryParser.KW_START - 128)) | (1 << (XQueryParser.KW_STRICT - 128)) | (1 << (XQueryParser.KW_STRIP - 128)) | (1 << (XQueryParser.KW_SWITCH - 128)) | (1 << (XQueryParser.KW_TEXT - 128)) | (1 << (XQueryParser.KW_THEN - 128)) | (1 << (XQueryParser.KW_TO - 128)) | (1 << (XQueryParser.KW_TREAT - 128)) | (1 << (XQueryParser.KW_TRY - 128)) | (1 << (XQueryParser.KW_TUMBLING - 128)) | (1 << (XQueryParser.KW_TYPE - 128)) | (1 << (XQueryParser.KW_TYPESWITCH - 128)) | (1 << (XQueryParser.KW_UNION - 128)) | (1 << (XQueryParser.KW_UNORDERED - 128)) | (1 << (XQueryParser.KW_UPDATE - 128)) | (1 << (XQueryParser.KW_VALIDATE - 128)) | (1 << (XQueryParser.KW_VARIABLE - 128)) | (1 << (XQueryParser.KW_VERSION - 128)) | (1 << (XQueryParser.KW_WHEN - 128)) | (1 << (XQueryParser.KW_WHERE - 128)) | (1 << (XQueryParser.KW_WINDOW - 128)) | (1 << (XQueryParser.KW_XQUERY - 128)) | (1 << (XQueryParser.KW_ARRAY_NODE - 128)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 128)) | (1 << (XQueryParser.KW_NULL_NODE - 128)) | (1 << (XQueryParser.KW_NUMBER_NODE - 128)) | (1 << (XQueryParser.KW_OBJECT_NODE - 128)) | (1 << (XQueryParser.KW_REPLACE - 128)) | (1 << (XQueryParser.KW_WITH - 128)) | (1 << (XQueryParser.KW_VALUE - 128)) | (1 << (XQueryParser.KW_INSERT - 128)) | (1 << (XQueryParser.KW_INTO - 128)) | (1 << (XQueryParser.KW_DELETE - 128)) | (1 << (XQueryParser.KW_RENAME - 128)) | (1 << (XQueryParser.URIQualifiedName - 128)) | (1 << (XQueryParser.FullQName - 128)) | (1 << (XQueryParser.NCName - 128)))) != 0):
                self.state = 1959
                self.sequenceType()
                self.state = 1964
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==XQueryParser.COMMA:
                    self.state = 1960
                    self.match(XQueryParser.COMMA)
                    self.state = 1961
                    self.sequenceType()
                    self.state = 1966
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 1969
            self.match(XQueryParser.RPAREN)
            self.state = 1970
            self.match(XQueryParser.KW_AS)
            self.state = 1971
            self.sequenceType()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MapTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def anyMapTest(self):
            return self.getTypedRuleContext(XQueryParser.AnyMapTestContext,0)


        def typedMapTest(self):
            return self.getTypedRuleContext(XQueryParser.TypedMapTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mapTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMapTest" ):
                listener.enterMapTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMapTest" ):
                listener.exitMapTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMapTest" ):
                return visitor.visitMapTest(self)
            else:
                return visitor.visitChildren(self)




    def mapTest(self):

        localctx = XQueryParser.MapTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 424, self.RULE_mapTest)
        try:
            self.state = 1975
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,180,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1973
                self.anyMapTest()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1974
                self.typedMapTest()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnyMapTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_MAP(self):
            return self.getToken(XQueryParser.KW_MAP, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_anyMapTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnyMapTest" ):
                listener.enterAnyMapTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnyMapTest" ):
                listener.exitAnyMapTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnyMapTest" ):
                return visitor.visitAnyMapTest(self)
            else:
                return visitor.visitChildren(self)




    def anyMapTest(self):

        localctx = XQueryParser.AnyMapTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 426, self.RULE_anyMapTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1977
            self.match(XQueryParser.KW_MAP)
            self.state = 1978
            self.match(XQueryParser.LPAREN)
            self.state = 1979
            self.match(XQueryParser.STAR)
            self.state = 1980
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypedMapTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_MAP(self):
            return self.getToken(XQueryParser.KW_MAP, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def eqName(self):
            return self.getTypedRuleContext(XQueryParser.EqNameContext,0)


        def COMMA(self):
            return self.getToken(XQueryParser.COMMA, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_typedMapTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypedMapTest" ):
                listener.enterTypedMapTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypedMapTest" ):
                listener.exitTypedMapTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypedMapTest" ):
                return visitor.visitTypedMapTest(self)
            else:
                return visitor.visitChildren(self)




    def typedMapTest(self):

        localctx = XQueryParser.TypedMapTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 428, self.RULE_typedMapTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1982
            self.match(XQueryParser.KW_MAP)
            self.state = 1983
            self.match(XQueryParser.LPAREN)
            self.state = 1984
            self.eqName()
            self.state = 1985
            self.match(XQueryParser.COMMA)
            self.state = 1986
            self.sequenceType()
            self.state = 1987
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def anyArrayTest(self):
            return self.getTypedRuleContext(XQueryParser.AnyArrayTestContext,0)


        def typedArrayTest(self):
            return self.getTypedRuleContext(XQueryParser.TypedArrayTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_arrayTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayTest" ):
                listener.enterArrayTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayTest" ):
                listener.exitArrayTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayTest" ):
                return visitor.visitArrayTest(self)
            else:
                return visitor.visitChildren(self)




    def arrayTest(self):

        localctx = XQueryParser.ArrayTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 430, self.RULE_arrayTest)
        try:
            self.state = 1991
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,181,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1989
                self.anyArrayTest()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1990
                self.typedArrayTest()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnyArrayTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ARRAY(self):
            return self.getToken(XQueryParser.KW_ARRAY, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def STAR(self):
            return self.getToken(XQueryParser.STAR, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_anyArrayTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnyArrayTest" ):
                listener.enterAnyArrayTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnyArrayTest" ):
                listener.exitAnyArrayTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnyArrayTest" ):
                return visitor.visitAnyArrayTest(self)
            else:
                return visitor.visitChildren(self)




    def anyArrayTest(self):

        localctx = XQueryParser.AnyArrayTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 432, self.RULE_anyArrayTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1993
            self.match(XQueryParser.KW_ARRAY)
            self.state = 1994
            self.match(XQueryParser.LPAREN)
            self.state = 1995
            self.match(XQueryParser.STAR)
            self.state = 1996
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypedArrayTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ARRAY(self):
            return self.getToken(XQueryParser.KW_ARRAY, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def sequenceType(self):
            return self.getTypedRuleContext(XQueryParser.SequenceTypeContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_typedArrayTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypedArrayTest" ):
                listener.enterTypedArrayTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypedArrayTest" ):
                listener.exitTypedArrayTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypedArrayTest" ):
                return visitor.visitTypedArrayTest(self)
            else:
                return visitor.visitChildren(self)




    def typedArrayTest(self):

        localctx = XQueryParser.TypedArrayTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 434, self.RULE_typedArrayTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1998
            self.match(XQueryParser.KW_ARRAY)
            self.state = 1999
            self.match(XQueryParser.LPAREN)
            self.state = 2000
            self.sequenceType()
            self.state = 2001
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParenthesizedItemTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def itemType(self):
            return self.getTypedRuleContext(XQueryParser.ItemTypeContext,0)


        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_parenthesizedItemTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesizedItemTest" ):
                listener.enterParenthesizedItemTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesizedItemTest" ):
                listener.exitParenthesizedItemTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenthesizedItemTest" ):
                return visitor.visitParenthesizedItemTest(self)
            else:
                return visitor.visitChildren(self)




    def parenthesizedItemTest(self):

        localctx = XQueryParser.ParenthesizedItemTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 436, self.RULE_parenthesizedItemTest)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2003
            self.match(XQueryParser.LPAREN)
            self.state = 2004
            self.itemType()
            self.state = 2005
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def attributeName(self):
            return self.getTypedRuleContext(XQueryParser.AttributeNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_attributeDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeDeclaration" ):
                listener.enterAttributeDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeDeclaration" ):
                listener.exitAttributeDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeDeclaration" ):
                return visitor.visitAttributeDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def attributeDeclaration(self):

        localctx = XQueryParser.AttributeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 438, self.RULE_attributeDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2007
            self.attributeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MlNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mlArrayNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.MlArrayNodeTestContext,0)


        def mlObjectNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.MlObjectNodeTestContext,0)


        def mlNumberNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.MlNumberNodeTestContext,0)


        def mlBooleanNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.MlBooleanNodeTestContext,0)


        def mlNullNodeTest(self):
            return self.getTypedRuleContext(XQueryParser.MlNullNodeTestContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mlNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMlNodeTest" ):
                listener.enterMlNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMlNodeTest" ):
                listener.exitMlNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMlNodeTest" ):
                return visitor.visitMlNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def mlNodeTest(self):

        localctx = XQueryParser.MlNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 440, self.RULE_mlNodeTest)
        try:
            self.state = 2014
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_ARRAY_NODE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2009
                self.mlArrayNodeTest()
                pass
            elif token in [XQueryParser.KW_OBJECT_NODE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2010
                self.mlObjectNodeTest()
                pass
            elif token in [XQueryParser.KW_NUMBER_NODE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 2011
                self.mlNumberNodeTest()
                pass
            elif token in [XQueryParser.KW_BOOLEAN_NODE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 2012
                self.mlBooleanNodeTest()
                pass
            elif token in [XQueryParser.KW_NULL_NODE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 2013
                self.mlNullNodeTest()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MlArrayNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ARRAY_NODE(self):
            return self.getToken(XQueryParser.KW_ARRAY_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mlArrayNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMlArrayNodeTest" ):
                listener.enterMlArrayNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMlArrayNodeTest" ):
                listener.exitMlArrayNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMlArrayNodeTest" ):
                return visitor.visitMlArrayNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def mlArrayNodeTest(self):

        localctx = XQueryParser.MlArrayNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 442, self.RULE_mlArrayNodeTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2016
            self.match(XQueryParser.KW_ARRAY_NODE)
            self.state = 2017
            self.match(XQueryParser.LPAREN)
            self.state = 2019
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.Quot or _la==XQueryParser.Apos:
                self.state = 2018
                self.stringLiteral()


            self.state = 2021
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MlObjectNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_OBJECT_NODE(self):
            return self.getToken(XQueryParser.KW_OBJECT_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mlObjectNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMlObjectNodeTest" ):
                listener.enterMlObjectNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMlObjectNodeTest" ):
                listener.exitMlObjectNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMlObjectNodeTest" ):
                return visitor.visitMlObjectNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def mlObjectNodeTest(self):

        localctx = XQueryParser.MlObjectNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 444, self.RULE_mlObjectNodeTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2023
            self.match(XQueryParser.KW_OBJECT_NODE)
            self.state = 2024
            self.match(XQueryParser.LPAREN)
            self.state = 2026
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.Quot or _la==XQueryParser.Apos:
                self.state = 2025
                self.stringLiteral()


            self.state = 2028
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MlNumberNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NUMBER_NODE(self):
            return self.getToken(XQueryParser.KW_NUMBER_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mlNumberNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMlNumberNodeTest" ):
                listener.enterMlNumberNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMlNumberNodeTest" ):
                listener.exitMlNumberNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMlNumberNodeTest" ):
                return visitor.visitMlNumberNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def mlNumberNodeTest(self):

        localctx = XQueryParser.MlNumberNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 446, self.RULE_mlNumberNodeTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2030
            self.match(XQueryParser.KW_NUMBER_NODE)
            self.state = 2031
            self.match(XQueryParser.LPAREN)
            self.state = 2033
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.Quot or _la==XQueryParser.Apos:
                self.state = 2032
                self.stringLiteral()


            self.state = 2035
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MlBooleanNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_BOOLEAN_NODE(self):
            return self.getToken(XQueryParser.KW_BOOLEAN_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mlBooleanNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMlBooleanNodeTest" ):
                listener.enterMlBooleanNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMlBooleanNodeTest" ):
                listener.exitMlBooleanNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMlBooleanNodeTest" ):
                return visitor.visitMlBooleanNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def mlBooleanNodeTest(self):

        localctx = XQueryParser.MlBooleanNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 448, self.RULE_mlBooleanNodeTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2037
            self.match(XQueryParser.KW_BOOLEAN_NODE)
            self.state = 2038
            self.match(XQueryParser.LPAREN)
            self.state = 2040
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.Quot or _la==XQueryParser.Apos:
                self.state = 2039
                self.stringLiteral()


            self.state = 2042
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MlNullNodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_NULL_NODE(self):
            return self.getToken(XQueryParser.KW_NULL_NODE, 0)

        def LPAREN(self):
            return self.getToken(XQueryParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(XQueryParser.RPAREN, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_mlNullNodeTest

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMlNullNodeTest" ):
                listener.enterMlNullNodeTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMlNullNodeTest" ):
                listener.exitMlNullNodeTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMlNullNodeTest" ):
                return visitor.visitMlNullNodeTest(self)
            else:
                return visitor.visitChildren(self)




    def mlNullNodeTest(self):

        localctx = XQueryParser.MlNullNodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 450, self.RULE_mlNullNodeTest)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2044
            self.match(XQueryParser.KW_NULL_NODE)
            self.state = 2045
            self.match(XQueryParser.LPAREN)
            self.state = 2047
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==XQueryParser.Quot or _la==XQueryParser.Apos:
                self.state = 2046
                self.stringLiteral()


            self.state = 2049
            self.match(XQueryParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EqNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qName(self):
            return self.getTypedRuleContext(XQueryParser.QNameContext,0)


        def URIQualifiedName(self):
            return self.getToken(XQueryParser.URIQualifiedName, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_eqName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqName" ):
                listener.enterEqName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqName" ):
                listener.exitEqName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqName" ):
                return visitor.visitEqName(self)
            else:
                return visitor.visitChildren(self)




    def eqName(self):

        localctx = XQueryParser.EqNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 452, self.RULE_eqName)
        try:
            self.state = 2053
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.FullQName, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2051
                self.qName()
                pass
            elif token in [XQueryParser.URIQualifiedName]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2052
                self.match(XQueryParser.URIQualifiedName)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FullQName(self):
            return self.getToken(XQueryParser.FullQName, 0)

        def ncName(self):
            return self.getTypedRuleContext(XQueryParser.NcNameContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_qName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQName" ):
                listener.enterQName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQName" ):
                listener.exitQName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQName" ):
                return visitor.visitQName(self)
            else:
                return visitor.visitChildren(self)




    def qName(self):

        localctx = XQueryParser.QNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 454, self.RULE_qName)
        try:
            self.state = 2057
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.FullQName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2055
                self.match(XQueryParser.FullQName)
                pass
            elif token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2056
                self.ncName()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NcNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NCName(self):
            return self.getToken(XQueryParser.NCName, 0)

        def keyword(self):
            return self.getTypedRuleContext(XQueryParser.KeywordContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_ncName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNcName" ):
                listener.enterNcName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNcName" ):
                listener.exitNcName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNcName" ):
                return visitor.visitNcName(self)
            else:
                return visitor.visitChildren(self)




    def ncName(self):

        localctx = XQueryParser.NcNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 456, self.RULE_ncName)
        try:
            self.state = 2061
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2059
                self.match(XQueryParser.NCName)
                pass
            elif token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2060
                self.keyword()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FullQName(self):
            return self.getToken(XQueryParser.FullQName, 0)

        def NCName(self):
            return self.getToken(XQueryParser.NCName, 0)

        def URIQualifiedName(self):
            return self.getToken(XQueryParser.URIQualifiedName, 0)

        def keywordOKForFunction(self):
            return self.getTypedRuleContext(XQueryParser.KeywordOKForFunctionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_functionName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionName" ):
                listener.enterFunctionName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionName" ):
                listener.exitFunctionName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionName" ):
                return visitor.visitFunctionName(self)
            else:
                return visitor.visitChildren(self)




    def functionName(self):

        localctx = XQueryParser.FunctionNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 458, self.RULE_functionName)
        try:
            self.state = 2067
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.FullQName]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2063
                self.match(XQueryParser.FullQName)
                pass
            elif token in [XQueryParser.NCName]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2064
                self.match(XQueryParser.NCName)
                pass
            elif token in [XQueryParser.URIQualifiedName]:
                self.enterOuterAlt(localctx, 3)
                self.state = 2065
                self.match(XQueryParser.URIQualifiedName)
                pass
            elif token in [XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_COPY_NS, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_ENCODING, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_OF, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SELF, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHERE, XQueryParser.KW_XQUERY]:
                self.enterOuterAlt(localctx, 4)
                self.state = 2066
                self.keywordOKForFunction()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeywordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def keywordOKForFunction(self):
            return self.getTypedRuleContext(XQueryParser.KeywordOKForFunctionContext,0)


        def keywordNotOKForFunction(self):
            return self.getTypedRuleContext(XQueryParser.KeywordNotOKForFunctionContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_keyword

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeyword" ):
                listener.enterKeyword(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeyword" ):
                listener.exitKeyword(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeyword" ):
                return visitor.visitKeyword(self)
            else:
                return visitor.visitChildren(self)




    def keyword(self):

        localctx = XQueryParser.KeywordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 460, self.RULE_keyword)
        try:
            self.state = 2071
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_COPY_NS, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_ENCODING, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_OF, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SELF, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHERE, XQueryParser.KW_XQUERY]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2069
                self.keywordOKForFunction()
                pass
            elif token in [XQueryParser.DFPropertyName, XQueryParser.KW_ALLOWING, XQueryParser.KW_ARRAY, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BINARY, XQueryParser.KW_CATCH, XQueryParser.KW_COMMENT, XQueryParser.KW_CONTEXT, XQueryParser.KW_COUNT, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_END, XQueryParser.KW_IF, XQueryParser.KW_ITEM, XQueryParser.KW_MAP, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NODE, XQueryParser.KW_ONLY, XQueryParser.KW_PI, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SLIDING, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UPDATE, XQueryParser.KW_WHEN, XQueryParser.KW_WINDOW, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2070
                self.keywordNotOKForFunction()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeywordNotOKForFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ATTRIBUTE(self):
            return self.getToken(XQueryParser.KW_ATTRIBUTE, 0)

        def KW_COMMENT(self):
            return self.getToken(XQueryParser.KW_COMMENT, 0)

        def KW_DOCUMENT_NODE(self):
            return self.getToken(XQueryParser.KW_DOCUMENT_NODE, 0)

        def KW_ELEMENT(self):
            return self.getToken(XQueryParser.KW_ELEMENT, 0)

        def KW_EMPTY_SEQUENCE(self):
            return self.getToken(XQueryParser.KW_EMPTY_SEQUENCE, 0)

        def KW_IF(self):
            return self.getToken(XQueryParser.KW_IF, 0)

        def KW_ITEM(self):
            return self.getToken(XQueryParser.KW_ITEM, 0)

        def KW_CONTEXT(self):
            return self.getToken(XQueryParser.KW_CONTEXT, 0)

        def KW_NODE(self):
            return self.getToken(XQueryParser.KW_NODE, 0)

        def KW_PI(self):
            return self.getToken(XQueryParser.KW_PI, 0)

        def KW_SCHEMA_ATTR(self):
            return self.getToken(XQueryParser.KW_SCHEMA_ATTR, 0)

        def KW_SCHEMA_ELEM(self):
            return self.getToken(XQueryParser.KW_SCHEMA_ELEM, 0)

        def KW_BINARY(self):
            return self.getToken(XQueryParser.KW_BINARY, 0)

        def KW_TEXT(self):
            return self.getToken(XQueryParser.KW_TEXT, 0)

        def KW_TYPESWITCH(self):
            return self.getToken(XQueryParser.KW_TYPESWITCH, 0)

        def KW_SWITCH(self):
            return self.getToken(XQueryParser.KW_SWITCH, 0)

        def KW_NAMESPACE_NODE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE_NODE, 0)

        def KW_TYPE(self):
            return self.getToken(XQueryParser.KW_TYPE, 0)

        def KW_TUMBLING(self):
            return self.getToken(XQueryParser.KW_TUMBLING, 0)

        def KW_TRY(self):
            return self.getToken(XQueryParser.KW_TRY, 0)

        def KW_CATCH(self):
            return self.getToken(XQueryParser.KW_CATCH, 0)

        def KW_ONLY(self):
            return self.getToken(XQueryParser.KW_ONLY, 0)

        def KW_WHEN(self):
            return self.getToken(XQueryParser.KW_WHEN, 0)

        def KW_SLIDING(self):
            return self.getToken(XQueryParser.KW_SLIDING, 0)

        def KW_DECIMAL_FORMAT(self):
            return self.getToken(XQueryParser.KW_DECIMAL_FORMAT, 0)

        def KW_WINDOW(self):
            return self.getToken(XQueryParser.KW_WINDOW, 0)

        def KW_COUNT(self):
            return self.getToken(XQueryParser.KW_COUNT, 0)

        def KW_MAP(self):
            return self.getToken(XQueryParser.KW_MAP, 0)

        def KW_END(self):
            return self.getToken(XQueryParser.KW_END, 0)

        def KW_ALLOWING(self):
            return self.getToken(XQueryParser.KW_ALLOWING, 0)

        def KW_ARRAY(self):
            return self.getToken(XQueryParser.KW_ARRAY, 0)

        def DFPropertyName(self):
            return self.getToken(XQueryParser.DFPropertyName, 0)

        def KW_ARRAY_NODE(self):
            return self.getToken(XQueryParser.KW_ARRAY_NODE, 0)

        def KW_BOOLEAN_NODE(self):
            return self.getToken(XQueryParser.KW_BOOLEAN_NODE, 0)

        def KW_NULL_NODE(self):
            return self.getToken(XQueryParser.KW_NULL_NODE, 0)

        def KW_NUMBER_NODE(self):
            return self.getToken(XQueryParser.KW_NUMBER_NODE, 0)

        def KW_OBJECT_NODE(self):
            return self.getToken(XQueryParser.KW_OBJECT_NODE, 0)

        def KW_UPDATE(self):
            return self.getToken(XQueryParser.KW_UPDATE, 0)

        def KW_REPLACE(self):
            return self.getToken(XQueryParser.KW_REPLACE, 0)

        def KW_WITH(self):
            return self.getToken(XQueryParser.KW_WITH, 0)

        def KW_VALUE(self):
            return self.getToken(XQueryParser.KW_VALUE, 0)

        def KW_INSERT(self):
            return self.getToken(XQueryParser.KW_INSERT, 0)

        def KW_INTO(self):
            return self.getToken(XQueryParser.KW_INTO, 0)

        def KW_DELETE(self):
            return self.getToken(XQueryParser.KW_DELETE, 0)

        def KW_NEXT(self):
            return self.getToken(XQueryParser.KW_NEXT, 0)

        def KW_RENAME(self):
            return self.getToken(XQueryParser.KW_RENAME, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_keywordNotOKForFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeywordNotOKForFunction" ):
                listener.enterKeywordNotOKForFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeywordNotOKForFunction" ):
                listener.exitKeywordNotOKForFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeywordNotOKForFunction" ):
                return visitor.visitKeywordNotOKForFunction(self)
            else:
                return visitor.visitChildren(self)




    def keywordNotOKForFunction(self):

        localctx = XQueryParser.KeywordNotOKForFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 462, self.RULE_keywordNotOKForFunction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2073
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_ATTRIBUTE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (XQueryParser.KW_ONLY - 129)) | (1 << (XQueryParser.KW_PI - 129)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 129)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 129)) | (1 << (XQueryParser.KW_SLIDING - 129)) | (1 << (XQueryParser.KW_SWITCH - 129)) | (1 << (XQueryParser.KW_TEXT - 129)) | (1 << (XQueryParser.KW_TRY - 129)) | (1 << (XQueryParser.KW_TUMBLING - 129)) | (1 << (XQueryParser.KW_TYPE - 129)) | (1 << (XQueryParser.KW_TYPESWITCH - 129)) | (1 << (XQueryParser.KW_UPDATE - 129)) | (1 << (XQueryParser.KW_WHEN - 129)) | (1 << (XQueryParser.KW_WINDOW - 129)) | (1 << (XQueryParser.KW_ARRAY_NODE - 129)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 129)) | (1 << (XQueryParser.KW_NULL_NODE - 129)) | (1 << (XQueryParser.KW_NUMBER_NODE - 129)) | (1 << (XQueryParser.KW_OBJECT_NODE - 129)) | (1 << (XQueryParser.KW_REPLACE - 129)) | (1 << (XQueryParser.KW_WITH - 129)) | (1 << (XQueryParser.KW_VALUE - 129)) | (1 << (XQueryParser.KW_INSERT - 129)) | (1 << (XQueryParser.KW_INTO - 129)) | (1 << (XQueryParser.KW_DELETE - 129)) | (1 << (XQueryParser.KW_RENAME - 129)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeywordOKForFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KW_ANCESTOR(self):
            return self.getToken(XQueryParser.KW_ANCESTOR, 0)

        def KW_ANCESTOR_OR_SELF(self):
            return self.getToken(XQueryParser.KW_ANCESTOR_OR_SELF, 0)

        def KW_AND(self):
            return self.getToken(XQueryParser.KW_AND, 0)

        def KW_AS(self):
            return self.getToken(XQueryParser.KW_AS, 0)

        def KW_ASCENDING(self):
            return self.getToken(XQueryParser.KW_ASCENDING, 0)

        def KW_AT(self):
            return self.getToken(XQueryParser.KW_AT, 0)

        def KW_BASE_URI(self):
            return self.getToken(XQueryParser.KW_BASE_URI, 0)

        def KW_BOUNDARY_SPACE(self):
            return self.getToken(XQueryParser.KW_BOUNDARY_SPACE, 0)

        def KW_BY(self):
            return self.getToken(XQueryParser.KW_BY, 0)

        def KW_CASE(self):
            return self.getToken(XQueryParser.KW_CASE, 0)

        def KW_CAST(self):
            return self.getToken(XQueryParser.KW_CAST, 0)

        def KW_CASTABLE(self):
            return self.getToken(XQueryParser.KW_CASTABLE, 0)

        def KW_CHILD(self):
            return self.getToken(XQueryParser.KW_CHILD, 0)

        def KW_COLLATION(self):
            return self.getToken(XQueryParser.KW_COLLATION, 0)

        def KW_CONSTRUCTION(self):
            return self.getToken(XQueryParser.KW_CONSTRUCTION, 0)

        def KW_COPY_NS(self):
            return self.getToken(XQueryParser.KW_COPY_NS, 0)

        def KW_DECLARE(self):
            return self.getToken(XQueryParser.KW_DECLARE, 0)

        def KW_DEFAULT(self):
            return self.getToken(XQueryParser.KW_DEFAULT, 0)

        def KW_DESCENDANT(self):
            return self.getToken(XQueryParser.KW_DESCENDANT, 0)

        def KW_DESCENDANT_OR_SELF(self):
            return self.getToken(XQueryParser.KW_DESCENDANT_OR_SELF, 0)

        def KW_DESCENDING(self):
            return self.getToken(XQueryParser.KW_DESCENDING, 0)

        def KW_DIV(self):
            return self.getToken(XQueryParser.KW_DIV, 0)

        def KW_DOCUMENT(self):
            return self.getToken(XQueryParser.KW_DOCUMENT, 0)

        def KW_ELSE(self):
            return self.getToken(XQueryParser.KW_ELSE, 0)

        def KW_EMPTY(self):
            return self.getToken(XQueryParser.KW_EMPTY, 0)

        def KW_ENCODING(self):
            return self.getToken(XQueryParser.KW_ENCODING, 0)

        def KW_EQ(self):
            return self.getToken(XQueryParser.KW_EQ, 0)

        def KW_EVERY(self):
            return self.getToken(XQueryParser.KW_EVERY, 0)

        def KW_EXCEPT(self):
            return self.getToken(XQueryParser.KW_EXCEPT, 0)

        def KW_EXTERNAL(self):
            return self.getToken(XQueryParser.KW_EXTERNAL, 0)

        def KW_FOLLOWING(self):
            return self.getToken(XQueryParser.KW_FOLLOWING, 0)

        def KW_FOLLOWING_SIBLING(self):
            return self.getToken(XQueryParser.KW_FOLLOWING_SIBLING, 0)

        def KW_FOR(self):
            return self.getToken(XQueryParser.KW_FOR, 0)

        def KW_FUNCTION(self):
            return self.getToken(XQueryParser.KW_FUNCTION, 0)

        def KW_GE(self):
            return self.getToken(XQueryParser.KW_GE, 0)

        def KW_GREATEST(self):
            return self.getToken(XQueryParser.KW_GREATEST, 0)

        def KW_GROUP(self):
            return self.getToken(XQueryParser.KW_GROUP, 0)

        def KW_GT(self):
            return self.getToken(XQueryParser.KW_GT, 0)

        def KW_IDIV(self):
            return self.getToken(XQueryParser.KW_IDIV, 0)

        def KW_IMPORT(self):
            return self.getToken(XQueryParser.KW_IMPORT, 0)

        def KW_IN(self):
            return self.getToken(XQueryParser.KW_IN, 0)

        def KW_INHERIT(self):
            return self.getToken(XQueryParser.KW_INHERIT, 0)

        def KW_INSTANCE(self):
            return self.getToken(XQueryParser.KW_INSTANCE, 0)

        def KW_INTERSECT(self):
            return self.getToken(XQueryParser.KW_INTERSECT, 0)

        def KW_IS(self):
            return self.getToken(XQueryParser.KW_IS, 0)

        def KW_LAX(self):
            return self.getToken(XQueryParser.KW_LAX, 0)

        def KW_LE(self):
            return self.getToken(XQueryParser.KW_LE, 0)

        def KW_LEAST(self):
            return self.getToken(XQueryParser.KW_LEAST, 0)

        def KW_LET(self):
            return self.getToken(XQueryParser.KW_LET, 0)

        def KW_LT(self):
            return self.getToken(XQueryParser.KW_LT, 0)

        def KW_MOD(self):
            return self.getToken(XQueryParser.KW_MOD, 0)

        def KW_MODULE(self):
            return self.getToken(XQueryParser.KW_MODULE, 0)

        def KW_NAMESPACE(self):
            return self.getToken(XQueryParser.KW_NAMESPACE, 0)

        def KW_NE(self):
            return self.getToken(XQueryParser.KW_NE, 0)

        def KW_NO_INHERIT(self):
            return self.getToken(XQueryParser.KW_NO_INHERIT, 0)

        def KW_NO_PRESERVE(self):
            return self.getToken(XQueryParser.KW_NO_PRESERVE, 0)

        def KW_OF(self):
            return self.getToken(XQueryParser.KW_OF, 0)

        def KW_OPTION(self):
            return self.getToken(XQueryParser.KW_OPTION, 0)

        def KW_OR(self):
            return self.getToken(XQueryParser.KW_OR, 0)

        def KW_ORDER(self):
            return self.getToken(XQueryParser.KW_ORDER, 0)

        def KW_ORDERED(self):
            return self.getToken(XQueryParser.KW_ORDERED, 0)

        def KW_ORDERING(self):
            return self.getToken(XQueryParser.KW_ORDERING, 0)

        def KW_PARENT(self):
            return self.getToken(XQueryParser.KW_PARENT, 0)

        def KW_PRECEDING(self):
            return self.getToken(XQueryParser.KW_PRECEDING, 0)

        def KW_PRECEDING_SIBLING(self):
            return self.getToken(XQueryParser.KW_PRECEDING_SIBLING, 0)

        def KW_PRESERVE(self):
            return self.getToken(XQueryParser.KW_PRESERVE, 0)

        def KW_RETURN(self):
            return self.getToken(XQueryParser.KW_RETURN, 0)

        def KW_SATISFIES(self):
            return self.getToken(XQueryParser.KW_SATISFIES, 0)

        def KW_SCHEMA(self):
            return self.getToken(XQueryParser.KW_SCHEMA, 0)

        def KW_SELF(self):
            return self.getToken(XQueryParser.KW_SELF, 0)

        def KW_SOME(self):
            return self.getToken(XQueryParser.KW_SOME, 0)

        def KW_STABLE(self):
            return self.getToken(XQueryParser.KW_STABLE, 0)

        def KW_START(self):
            return self.getToken(XQueryParser.KW_START, 0)

        def KW_STRICT(self):
            return self.getToken(XQueryParser.KW_STRICT, 0)

        def KW_STRIP(self):
            return self.getToken(XQueryParser.KW_STRIP, 0)

        def KW_THEN(self):
            return self.getToken(XQueryParser.KW_THEN, 0)

        def KW_TO(self):
            return self.getToken(XQueryParser.KW_TO, 0)

        def KW_TREAT(self):
            return self.getToken(XQueryParser.KW_TREAT, 0)

        def KW_UNION(self):
            return self.getToken(XQueryParser.KW_UNION, 0)

        def KW_UNORDERED(self):
            return self.getToken(XQueryParser.KW_UNORDERED, 0)

        def KW_VALIDATE(self):
            return self.getToken(XQueryParser.KW_VALIDATE, 0)

        def KW_VARIABLE(self):
            return self.getToken(XQueryParser.KW_VARIABLE, 0)

        def KW_VERSION(self):
            return self.getToken(XQueryParser.KW_VERSION, 0)

        def KW_WHERE(self):
            return self.getToken(XQueryParser.KW_WHERE, 0)

        def KW_XQUERY(self):
            return self.getToken(XQueryParser.KW_XQUERY, 0)

        def getRuleIndex(self):
            return XQueryParser.RULE_keywordOKForFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeywordOKForFunction" ):
                listener.enterKeywordOKForFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeywordOKForFunction" ):
                listener.exitKeywordOKForFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeywordOKForFunction" ):
                return visitor.visitKeywordOKForFunction(self)
            else:
                return visitor.visitChildren(self)




    def keywordOKForFunction(self):

        localctx = XQueryParser.KeywordOKForFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 464, self.RULE_keywordOKForFunction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2075
            _la = self._input.LA(1)
            if not(((((_la - 54)) & ~0x3f) == 0 and ((1 << (_la - 54)) & ((1 << (XQueryParser.KW_ANCESTOR - 54)) | (1 << (XQueryParser.KW_ANCESTOR_OR_SELF - 54)) | (1 << (XQueryParser.KW_AND - 54)) | (1 << (XQueryParser.KW_AS - 54)) | (1 << (XQueryParser.KW_ASCENDING - 54)) | (1 << (XQueryParser.KW_AT - 54)) | (1 << (XQueryParser.KW_BASE_URI - 54)) | (1 << (XQueryParser.KW_BOUNDARY_SPACE - 54)) | (1 << (XQueryParser.KW_BY - 54)) | (1 << (XQueryParser.KW_CASE - 54)) | (1 << (XQueryParser.KW_CAST - 54)) | (1 << (XQueryParser.KW_CASTABLE - 54)) | (1 << (XQueryParser.KW_CHILD - 54)) | (1 << (XQueryParser.KW_COLLATION - 54)) | (1 << (XQueryParser.KW_CONSTRUCTION - 54)) | (1 << (XQueryParser.KW_COPY_NS - 54)) | (1 << (XQueryParser.KW_DECLARE - 54)) | (1 << (XQueryParser.KW_DEFAULT - 54)) | (1 << (XQueryParser.KW_DESCENDANT - 54)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 54)) | (1 << (XQueryParser.KW_DESCENDING - 54)) | (1 << (XQueryParser.KW_DIV - 54)) | (1 << (XQueryParser.KW_DOCUMENT - 54)) | (1 << (XQueryParser.KW_ELSE - 54)) | (1 << (XQueryParser.KW_EMPTY - 54)) | (1 << (XQueryParser.KW_ENCODING - 54)) | (1 << (XQueryParser.KW_EQ - 54)) | (1 << (XQueryParser.KW_EVERY - 54)) | (1 << (XQueryParser.KW_EXCEPT - 54)) | (1 << (XQueryParser.KW_EXTERNAL - 54)) | (1 << (XQueryParser.KW_FOLLOWING - 54)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 54)) | (1 << (XQueryParser.KW_FOR - 54)) | (1 << (XQueryParser.KW_FUNCTION - 54)) | (1 << (XQueryParser.KW_GE - 54)) | (1 << (XQueryParser.KW_GREATEST - 54)) | (1 << (XQueryParser.KW_GROUP - 54)) | (1 << (XQueryParser.KW_GT - 54)) | (1 << (XQueryParser.KW_IDIV - 54)) | (1 << (XQueryParser.KW_IMPORT - 54)) | (1 << (XQueryParser.KW_IN - 54)) | (1 << (XQueryParser.KW_INHERIT - 54)) | (1 << (XQueryParser.KW_INSTANCE - 54)) | (1 << (XQueryParser.KW_INTERSECT - 54)) | (1 << (XQueryParser.KW_IS - 54)) | (1 << (XQueryParser.KW_LAX - 54)) | (1 << (XQueryParser.KW_LE - 54)) | (1 << (XQueryParser.KW_LEAST - 54)) | (1 << (XQueryParser.KW_LET - 54)) | (1 << (XQueryParser.KW_LT - 54)))) != 0) or ((((_la - 119)) & ~0x3f) == 0 and ((1 << (_la - 119)) & ((1 << (XQueryParser.KW_MOD - 119)) | (1 << (XQueryParser.KW_MODULE - 119)) | (1 << (XQueryParser.KW_NAMESPACE - 119)) | (1 << (XQueryParser.KW_NE - 119)) | (1 << (XQueryParser.KW_NO_INHERIT - 119)) | (1 << (XQueryParser.KW_NO_PRESERVE - 119)) | (1 << (XQueryParser.KW_OF - 119)) | (1 << (XQueryParser.KW_OPTION - 119)) | (1 << (XQueryParser.KW_OR - 119)) | (1 << (XQueryParser.KW_ORDER - 119)) | (1 << (XQueryParser.KW_ORDERED - 119)) | (1 << (XQueryParser.KW_ORDERING - 119)) | (1 << (XQueryParser.KW_PARENT - 119)) | (1 << (XQueryParser.KW_PRECEDING - 119)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 119)) | (1 << (XQueryParser.KW_PRESERVE - 119)) | (1 << (XQueryParser.KW_RETURN - 119)) | (1 << (XQueryParser.KW_SATISFIES - 119)) | (1 << (XQueryParser.KW_SCHEMA - 119)) | (1 << (XQueryParser.KW_SELF - 119)) | (1 << (XQueryParser.KW_SOME - 119)) | (1 << (XQueryParser.KW_STABLE - 119)) | (1 << (XQueryParser.KW_START - 119)) | (1 << (XQueryParser.KW_STRICT - 119)) | (1 << (XQueryParser.KW_STRIP - 119)) | (1 << (XQueryParser.KW_THEN - 119)) | (1 << (XQueryParser.KW_TO - 119)) | (1 << (XQueryParser.KW_TREAT - 119)) | (1 << (XQueryParser.KW_UNION - 119)) | (1 << (XQueryParser.KW_UNORDERED - 119)) | (1 << (XQueryParser.KW_VALIDATE - 119)) | (1 << (XQueryParser.KW_VARIABLE - 119)) | (1 << (XQueryParser.KW_VERSION - 119)) | (1 << (XQueryParser.KW_WHERE - 119)) | (1 << (XQueryParser.KW_XQUERY - 119)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UriLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringLiteral(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_uriLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUriLiteral" ):
                listener.enterUriLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUriLiteral" ):
                listener.exitUriLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUriLiteral" ):
                return visitor.visitUriLiteral(self)
            else:
                return visitor.visitChildren(self)




    def uriLiteral(self):

        localctx = XQueryParser.UriLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 466, self.RULE_uriLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2077
            self.stringLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringLiteralQuotContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Quot(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.Quot)
            else:
                return self.getToken(XQueryParser.Quot, i)

        def PredefinedEntityRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PredefinedEntityRef)
            else:
                return self.getToken(XQueryParser.PredefinedEntityRef, i)

        def CharRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.CharRef)
            else:
                return self.getToken(XQueryParser.CharRef, i)

        def EscapeQuot(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EscapeQuot)
            else:
                return self.getToken(XQueryParser.EscapeQuot, i)

        def stringContentQuot(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringContentQuotContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringContentQuotContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_stringLiteralQuot

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteralQuot" ):
                listener.enterStringLiteralQuot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteralQuot" ):
                listener.exitStringLiteralQuot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteralQuot" ):
                return visitor.visitStringLiteralQuot(self)
            else:
                return visitor.visitChildren(self)




    def stringLiteralQuot(self):

        localctx = XQueryParser.StringLiteralQuotContext(self, self._ctx, self.state)
        self.enterRule(localctx, 468, self.RULE_stringLiteralQuot)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2079
            self.match(XQueryParser.Quot)
            self.state = 2086
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.EscapeQuot) | (1 << XQueryParser.DOUBLE_LBRACE) | (1 << XQueryParser.DOUBLE_RBRACE) | (1 << XQueryParser.IntegerLiteral) | (1 << XQueryParser.DecimalLiteral) | (1 << XQueryParser.DoubleLiteral) | (1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.PredefinedEntityRef) | (1 << XQueryParser.CharRef) | (1 << XQueryParser.Apos) | (1 << XQueryParser.COMMENT) | (1 << XQueryParser.PRAGMA) | (1 << XQueryParser.EQUAL) | (1 << XQueryParser.NOT_EQUAL) | (1 << XQueryParser.LPAREN) | (1 << XQueryParser.RPAREN) | (1 << XQueryParser.LBRACKET) | (1 << XQueryParser.RBRACKET) | (1 << XQueryParser.LBRACE) | (1 << XQueryParser.RBRACE) | (1 << XQueryParser.STAR) | (1 << XQueryParser.PLUS) | (1 << XQueryParser.MINUS) | (1 << XQueryParser.COMMA) | (1 << XQueryParser.DOT) | (1 << XQueryParser.DDOT) | (1 << XQueryParser.COLON) | (1 << XQueryParser.COLON_EQ) | (1 << XQueryParser.SEMICOLON) | (1 << XQueryParser.SLASH) | (1 << XQueryParser.DSLASH) | (1 << XQueryParser.BACKSLASH) | (1 << XQueryParser.VBAR) | (1 << XQueryParser.RANGLE) | (1 << XQueryParser.QUESTION) | (1 << XQueryParser.AT) | (1 << XQueryParser.DOLLAR) | (1 << XQueryParser.MOD) | (1 << XQueryParser.BANG) | (1 << XQueryParser.HASH) | (1 << XQueryParser.CARAT) | (1 << XQueryParser.ARROW) | (1 << XQueryParser.GRAVE) | (1 << XQueryParser.TILDE) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ANCESTOR) | (1 << XQueryParser.KW_ANCESTOR_OR_SELF) | (1 << XQueryParser.KW_AND) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_AS) | (1 << XQueryParser.KW_ASCENDING) | (1 << XQueryParser.KW_AT) | (1 << XQueryParser.KW_ATTRIBUTE) | (1 << XQueryParser.KW_BASE_URI) | (1 << XQueryParser.KW_BOUNDARY_SPACE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_BY - 64)) | (1 << (XQueryParser.KW_CASE - 64)) | (1 << (XQueryParser.KW_CAST - 64)) | (1 << (XQueryParser.KW_CASTABLE - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_CHILD - 64)) | (1 << (XQueryParser.KW_COLLATION - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONSTRUCTION - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COPY_NS - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECLARE - 64)) | (1 << (XQueryParser.KW_DEFAULT - 64)) | (1 << (XQueryParser.KW_DESCENDANT - 64)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 64)) | (1 << (XQueryParser.KW_DESCENDING - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DIV - 64)) | (1 << (XQueryParser.KW_DOCUMENT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_ELSE - 64)) | (1 << (XQueryParser.KW_EMPTY - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_ENCODING - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_EQ - 64)) | (1 << (XQueryParser.KW_EVERY - 64)) | (1 << (XQueryParser.KW_EXCEPT - 64)) | (1 << (XQueryParser.KW_EXTERNAL - 64)) | (1 << (XQueryParser.KW_FOLLOWING - 64)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 64)) | (1 << (XQueryParser.KW_FOR - 64)) | (1 << (XQueryParser.KW_FUNCTION - 64)) | (1 << (XQueryParser.KW_GE - 64)) | (1 << (XQueryParser.KW_GREATEST - 64)) | (1 << (XQueryParser.KW_GROUP - 64)) | (1 << (XQueryParser.KW_GT - 64)) | (1 << (XQueryParser.KW_IDIV - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_IMPORT - 64)) | (1 << (XQueryParser.KW_IN - 64)) | (1 << (XQueryParser.KW_INHERIT - 64)) | (1 << (XQueryParser.KW_INSTANCE - 64)) | (1 << (XQueryParser.KW_INTERSECT - 64)) | (1 << (XQueryParser.KW_IS - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_LAX - 64)) | (1 << (XQueryParser.KW_LE - 64)) | (1 << (XQueryParser.KW_LEAST - 64)) | (1 << (XQueryParser.KW_LET - 64)) | (1 << (XQueryParser.KW_LT - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_MOD - 64)) | (1 << (XQueryParser.KW_MODULE - 64)) | (1 << (XQueryParser.KW_NAMESPACE - 64)) | (1 << (XQueryParser.KW_NE - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NO_INHERIT - 64)) | (1 << (XQueryParser.KW_NO_PRESERVE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (XQueryParser.KW_OF - 128)) | (1 << (XQueryParser.KW_ONLY - 128)) | (1 << (XQueryParser.KW_OPTION - 128)) | (1 << (XQueryParser.KW_OR - 128)) | (1 << (XQueryParser.KW_ORDER - 128)) | (1 << (XQueryParser.KW_ORDERED - 128)) | (1 << (XQueryParser.KW_ORDERING - 128)) | (1 << (XQueryParser.KW_PARENT - 128)) | (1 << (XQueryParser.KW_PRECEDING - 128)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 128)) | (1 << (XQueryParser.KW_PRESERVE - 128)) | (1 << (XQueryParser.KW_PREVIOUS - 128)) | (1 << (XQueryParser.KW_PI - 128)) | (1 << (XQueryParser.KW_RETURN - 128)) | (1 << (XQueryParser.KW_SATISFIES - 128)) | (1 << (XQueryParser.KW_SCHEMA - 128)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 128)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 128)) | (1 << (XQueryParser.KW_SELF - 128)) | (1 << (XQueryParser.KW_SLIDING - 128)) | (1 << (XQueryParser.KW_SOME - 128)) | (1 << (XQueryParser.KW_STABLE - 128)) | (1 << (XQueryParser.KW_START - 128)) | (1 << (XQueryParser.KW_STRICT - 128)) | (1 << (XQueryParser.KW_STRIP - 128)) | (1 << (XQueryParser.KW_SWITCH - 128)) | (1 << (XQueryParser.KW_TEXT - 128)) | (1 << (XQueryParser.KW_THEN - 128)) | (1 << (XQueryParser.KW_TO - 128)) | (1 << (XQueryParser.KW_TREAT - 128)) | (1 << (XQueryParser.KW_TRY - 128)) | (1 << (XQueryParser.KW_TUMBLING - 128)) | (1 << (XQueryParser.KW_TYPE - 128)) | (1 << (XQueryParser.KW_TYPESWITCH - 128)) | (1 << (XQueryParser.KW_UNION - 128)) | (1 << (XQueryParser.KW_UNORDERED - 128)) | (1 << (XQueryParser.KW_UPDATE - 128)) | (1 << (XQueryParser.KW_VALIDATE - 128)) | (1 << (XQueryParser.KW_VARIABLE - 128)) | (1 << (XQueryParser.KW_VERSION - 128)) | (1 << (XQueryParser.KW_WHEN - 128)) | (1 << (XQueryParser.KW_WHERE - 128)) | (1 << (XQueryParser.KW_WINDOW - 128)) | (1 << (XQueryParser.KW_XQUERY - 128)) | (1 << (XQueryParser.KW_ARRAY_NODE - 128)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 128)) | (1 << (XQueryParser.KW_NULL_NODE - 128)) | (1 << (XQueryParser.KW_NUMBER_NODE - 128)) | (1 << (XQueryParser.KW_OBJECT_NODE - 128)) | (1 << (XQueryParser.KW_REPLACE - 128)) | (1 << (XQueryParser.KW_WITH - 128)) | (1 << (XQueryParser.KW_VALUE - 128)) | (1 << (XQueryParser.KW_INSERT - 128)) | (1 << (XQueryParser.KW_INTO - 128)) | (1 << (XQueryParser.KW_DELETE - 128)) | (1 << (XQueryParser.KW_RENAME - 128)) | (1 << (XQueryParser.URIQualifiedName - 128)) | (1 << (XQueryParser.FullQName - 128)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 128)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 128)) | (1 << (XQueryParser.NCName - 128)) | (1 << (XQueryParser.XQDOC_COMMENT_START - 128)))) != 0) or _la==XQueryParser.ContentChar:
                self.state = 2084
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [XQueryParser.PredefinedEntityRef]:
                    self.state = 2080
                    self.match(XQueryParser.PredefinedEntityRef)
                    pass
                elif token in [XQueryParser.CharRef]:
                    self.state = 2081
                    self.match(XQueryParser.CharRef)
                    pass
                elif token in [XQueryParser.EscapeQuot]:
                    self.state = 2082
                    self.match(XQueryParser.EscapeQuot)
                    pass
                elif token in [XQueryParser.DOUBLE_LBRACE, XQueryParser.DOUBLE_RBRACE, XQueryParser.IntegerLiteral, XQueryParser.DecimalLiteral, XQueryParser.DoubleLiteral, XQueryParser.DFPropertyName, XQueryParser.Apos, XQueryParser.COMMENT, XQueryParser.PRAGMA, XQueryParser.EQUAL, XQueryParser.NOT_EQUAL, XQueryParser.LPAREN, XQueryParser.RPAREN, XQueryParser.LBRACKET, XQueryParser.RBRACKET, XQueryParser.LBRACE, XQueryParser.RBRACE, XQueryParser.STAR, XQueryParser.PLUS, XQueryParser.MINUS, XQueryParser.COMMA, XQueryParser.DOT, XQueryParser.DDOT, XQueryParser.COLON, XQueryParser.COLON_EQ, XQueryParser.SEMICOLON, XQueryParser.SLASH, XQueryParser.DSLASH, XQueryParser.BACKSLASH, XQueryParser.VBAR, XQueryParser.RANGLE, XQueryParser.QUESTION, XQueryParser.AT, XQueryParser.DOLLAR, XQueryParser.MOD, XQueryParser.BANG, XQueryParser.HASH, XQueryParser.CARAT, XQueryParser.ARROW, XQueryParser.GRAVE, XQueryParser.TILDE, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PREVIOUS, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCNameWithLocalWildcard, XQueryParser.NCNameWithPrefixWildcard, XQueryParser.NCName, XQueryParser.XQDOC_COMMENT_START, XQueryParser.ContentChar]:
                    self.state = 2083
                    self.stringContentQuot()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 2088
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2089
            self.match(XQueryParser.Quot)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringLiteralAposContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Apos(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.Apos)
            else:
                return self.getToken(XQueryParser.Apos, i)

        def PredefinedEntityRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PredefinedEntityRef)
            else:
                return self.getToken(XQueryParser.PredefinedEntityRef, i)

        def CharRef(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.CharRef)
            else:
                return self.getToken(XQueryParser.CharRef, i)

        def EscapeApos(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EscapeApos)
            else:
                return self.getToken(XQueryParser.EscapeApos, i)

        def stringContentApos(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.StringContentAposContext)
            else:
                return self.getTypedRuleContext(XQueryParser.StringContentAposContext,i)


        def getRuleIndex(self):
            return XQueryParser.RULE_stringLiteralApos

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteralApos" ):
                listener.enterStringLiteralApos(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteralApos" ):
                listener.exitStringLiteralApos(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteralApos" ):
                return visitor.visitStringLiteralApos(self)
            else:
                return visitor.visitChildren(self)




    def stringLiteralApos(self):

        localctx = XQueryParser.StringLiteralAposContext(self, self._ctx, self.state)
        self.enterRule(localctx, 470, self.RULE_stringLiteralApos)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2091
            self.match(XQueryParser.Apos)
            self.state = 2098
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.EscapeApos) | (1 << XQueryParser.DOUBLE_LBRACE) | (1 << XQueryParser.DOUBLE_RBRACE) | (1 << XQueryParser.IntegerLiteral) | (1 << XQueryParser.DecimalLiteral) | (1 << XQueryParser.DoubleLiteral) | (1 << XQueryParser.DFPropertyName) | (1 << XQueryParser.PredefinedEntityRef) | (1 << XQueryParser.CharRef) | (1 << XQueryParser.Quot) | (1 << XQueryParser.COMMENT) | (1 << XQueryParser.PRAGMA) | (1 << XQueryParser.EQUAL) | (1 << XQueryParser.NOT_EQUAL) | (1 << XQueryParser.LPAREN) | (1 << XQueryParser.RPAREN) | (1 << XQueryParser.LBRACKET) | (1 << XQueryParser.RBRACKET) | (1 << XQueryParser.LBRACE) | (1 << XQueryParser.RBRACE) | (1 << XQueryParser.STAR) | (1 << XQueryParser.PLUS) | (1 << XQueryParser.MINUS) | (1 << XQueryParser.COMMA) | (1 << XQueryParser.DOT) | (1 << XQueryParser.DDOT) | (1 << XQueryParser.COLON) | (1 << XQueryParser.COLON_EQ) | (1 << XQueryParser.SEMICOLON) | (1 << XQueryParser.SLASH) | (1 << XQueryParser.DSLASH) | (1 << XQueryParser.BACKSLASH) | (1 << XQueryParser.VBAR) | (1 << XQueryParser.RANGLE) | (1 << XQueryParser.QUESTION) | (1 << XQueryParser.AT) | (1 << XQueryParser.DOLLAR) | (1 << XQueryParser.MOD) | (1 << XQueryParser.BANG) | (1 << XQueryParser.HASH) | (1 << XQueryParser.CARAT) | (1 << XQueryParser.ARROW) | (1 << XQueryParser.GRAVE) | (1 << XQueryParser.TILDE) | (1 << XQueryParser.KW_ALLOWING) | (1 << XQueryParser.KW_ANCESTOR) | (1 << XQueryParser.KW_ANCESTOR_OR_SELF) | (1 << XQueryParser.KW_AND) | (1 << XQueryParser.KW_ARRAY) | (1 << XQueryParser.KW_AS) | (1 << XQueryParser.KW_ASCENDING) | (1 << XQueryParser.KW_AT) | (1 << XQueryParser.KW_ATTRIBUTE) | (1 << XQueryParser.KW_BASE_URI) | (1 << XQueryParser.KW_BOUNDARY_SPACE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (XQueryParser.KW_BINARY - 64)) | (1 << (XQueryParser.KW_BY - 64)) | (1 << (XQueryParser.KW_CASE - 64)) | (1 << (XQueryParser.KW_CAST - 64)) | (1 << (XQueryParser.KW_CASTABLE - 64)) | (1 << (XQueryParser.KW_CATCH - 64)) | (1 << (XQueryParser.KW_CHILD - 64)) | (1 << (XQueryParser.KW_COLLATION - 64)) | (1 << (XQueryParser.KW_COMMENT - 64)) | (1 << (XQueryParser.KW_CONSTRUCTION - 64)) | (1 << (XQueryParser.KW_CONTEXT - 64)) | (1 << (XQueryParser.KW_COPY_NS - 64)) | (1 << (XQueryParser.KW_COUNT - 64)) | (1 << (XQueryParser.KW_DECLARE - 64)) | (1 << (XQueryParser.KW_DEFAULT - 64)) | (1 << (XQueryParser.KW_DESCENDANT - 64)) | (1 << (XQueryParser.KW_DESCENDANT_OR_SELF - 64)) | (1 << (XQueryParser.KW_DESCENDING - 64)) | (1 << (XQueryParser.KW_DECIMAL_FORMAT - 64)) | (1 << (XQueryParser.KW_DIV - 64)) | (1 << (XQueryParser.KW_DOCUMENT - 64)) | (1 << (XQueryParser.KW_DOCUMENT_NODE - 64)) | (1 << (XQueryParser.KW_ELEMENT - 64)) | (1 << (XQueryParser.KW_ELSE - 64)) | (1 << (XQueryParser.KW_EMPTY - 64)) | (1 << (XQueryParser.KW_EMPTY_SEQUENCE - 64)) | (1 << (XQueryParser.KW_ENCODING - 64)) | (1 << (XQueryParser.KW_END - 64)) | (1 << (XQueryParser.KW_EQ - 64)) | (1 << (XQueryParser.KW_EVERY - 64)) | (1 << (XQueryParser.KW_EXCEPT - 64)) | (1 << (XQueryParser.KW_EXTERNAL - 64)) | (1 << (XQueryParser.KW_FOLLOWING - 64)) | (1 << (XQueryParser.KW_FOLLOWING_SIBLING - 64)) | (1 << (XQueryParser.KW_FOR - 64)) | (1 << (XQueryParser.KW_FUNCTION - 64)) | (1 << (XQueryParser.KW_GE - 64)) | (1 << (XQueryParser.KW_GREATEST - 64)) | (1 << (XQueryParser.KW_GROUP - 64)) | (1 << (XQueryParser.KW_GT - 64)) | (1 << (XQueryParser.KW_IDIV - 64)) | (1 << (XQueryParser.KW_IF - 64)) | (1 << (XQueryParser.KW_IMPORT - 64)) | (1 << (XQueryParser.KW_IN - 64)) | (1 << (XQueryParser.KW_INHERIT - 64)) | (1 << (XQueryParser.KW_INSTANCE - 64)) | (1 << (XQueryParser.KW_INTERSECT - 64)) | (1 << (XQueryParser.KW_IS - 64)) | (1 << (XQueryParser.KW_ITEM - 64)) | (1 << (XQueryParser.KW_LAX - 64)) | (1 << (XQueryParser.KW_LE - 64)) | (1 << (XQueryParser.KW_LEAST - 64)) | (1 << (XQueryParser.KW_LET - 64)) | (1 << (XQueryParser.KW_LT - 64)) | (1 << (XQueryParser.KW_MAP - 64)) | (1 << (XQueryParser.KW_MOD - 64)) | (1 << (XQueryParser.KW_MODULE - 64)) | (1 << (XQueryParser.KW_NAMESPACE - 64)) | (1 << (XQueryParser.KW_NE - 64)) | (1 << (XQueryParser.KW_NEXT - 64)) | (1 << (XQueryParser.KW_NAMESPACE_NODE - 64)) | (1 << (XQueryParser.KW_NO_INHERIT - 64)) | (1 << (XQueryParser.KW_NO_PRESERVE - 64)) | (1 << (XQueryParser.KW_NODE - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (XQueryParser.KW_OF - 128)) | (1 << (XQueryParser.KW_ONLY - 128)) | (1 << (XQueryParser.KW_OPTION - 128)) | (1 << (XQueryParser.KW_OR - 128)) | (1 << (XQueryParser.KW_ORDER - 128)) | (1 << (XQueryParser.KW_ORDERED - 128)) | (1 << (XQueryParser.KW_ORDERING - 128)) | (1 << (XQueryParser.KW_PARENT - 128)) | (1 << (XQueryParser.KW_PRECEDING - 128)) | (1 << (XQueryParser.KW_PRECEDING_SIBLING - 128)) | (1 << (XQueryParser.KW_PRESERVE - 128)) | (1 << (XQueryParser.KW_PREVIOUS - 128)) | (1 << (XQueryParser.KW_PI - 128)) | (1 << (XQueryParser.KW_RETURN - 128)) | (1 << (XQueryParser.KW_SATISFIES - 128)) | (1 << (XQueryParser.KW_SCHEMA - 128)) | (1 << (XQueryParser.KW_SCHEMA_ATTR - 128)) | (1 << (XQueryParser.KW_SCHEMA_ELEM - 128)) | (1 << (XQueryParser.KW_SELF - 128)) | (1 << (XQueryParser.KW_SLIDING - 128)) | (1 << (XQueryParser.KW_SOME - 128)) | (1 << (XQueryParser.KW_STABLE - 128)) | (1 << (XQueryParser.KW_START - 128)) | (1 << (XQueryParser.KW_STRICT - 128)) | (1 << (XQueryParser.KW_STRIP - 128)) | (1 << (XQueryParser.KW_SWITCH - 128)) | (1 << (XQueryParser.KW_TEXT - 128)) | (1 << (XQueryParser.KW_THEN - 128)) | (1 << (XQueryParser.KW_TO - 128)) | (1 << (XQueryParser.KW_TREAT - 128)) | (1 << (XQueryParser.KW_TRY - 128)) | (1 << (XQueryParser.KW_TUMBLING - 128)) | (1 << (XQueryParser.KW_TYPE - 128)) | (1 << (XQueryParser.KW_TYPESWITCH - 128)) | (1 << (XQueryParser.KW_UNION - 128)) | (1 << (XQueryParser.KW_UNORDERED - 128)) | (1 << (XQueryParser.KW_UPDATE - 128)) | (1 << (XQueryParser.KW_VALIDATE - 128)) | (1 << (XQueryParser.KW_VARIABLE - 128)) | (1 << (XQueryParser.KW_VERSION - 128)) | (1 << (XQueryParser.KW_WHEN - 128)) | (1 << (XQueryParser.KW_WHERE - 128)) | (1 << (XQueryParser.KW_WINDOW - 128)) | (1 << (XQueryParser.KW_XQUERY - 128)) | (1 << (XQueryParser.KW_ARRAY_NODE - 128)) | (1 << (XQueryParser.KW_BOOLEAN_NODE - 128)) | (1 << (XQueryParser.KW_NULL_NODE - 128)) | (1 << (XQueryParser.KW_NUMBER_NODE - 128)) | (1 << (XQueryParser.KW_OBJECT_NODE - 128)) | (1 << (XQueryParser.KW_REPLACE - 128)) | (1 << (XQueryParser.KW_WITH - 128)) | (1 << (XQueryParser.KW_VALUE - 128)) | (1 << (XQueryParser.KW_INSERT - 128)) | (1 << (XQueryParser.KW_INTO - 128)) | (1 << (XQueryParser.KW_DELETE - 128)) | (1 << (XQueryParser.KW_RENAME - 128)) | (1 << (XQueryParser.URIQualifiedName - 128)) | (1 << (XQueryParser.FullQName - 128)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 128)) | (1 << (XQueryParser.NCNameWithPrefixWildcard - 128)) | (1 << (XQueryParser.NCName - 128)) | (1 << (XQueryParser.XQDOC_COMMENT_START - 128)))) != 0) or _la==XQueryParser.ContentChar:
                self.state = 2096
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [XQueryParser.PredefinedEntityRef]:
                    self.state = 2092
                    self.match(XQueryParser.PredefinedEntityRef)
                    pass
                elif token in [XQueryParser.CharRef]:
                    self.state = 2093
                    self.match(XQueryParser.CharRef)
                    pass
                elif token in [XQueryParser.EscapeApos]:
                    self.state = 2094
                    self.match(XQueryParser.EscapeApos)
                    pass
                elif token in [XQueryParser.DOUBLE_LBRACE, XQueryParser.DOUBLE_RBRACE, XQueryParser.IntegerLiteral, XQueryParser.DecimalLiteral, XQueryParser.DoubleLiteral, XQueryParser.DFPropertyName, XQueryParser.Quot, XQueryParser.COMMENT, XQueryParser.PRAGMA, XQueryParser.EQUAL, XQueryParser.NOT_EQUAL, XQueryParser.LPAREN, XQueryParser.RPAREN, XQueryParser.LBRACKET, XQueryParser.RBRACKET, XQueryParser.LBRACE, XQueryParser.RBRACE, XQueryParser.STAR, XQueryParser.PLUS, XQueryParser.MINUS, XQueryParser.COMMA, XQueryParser.DOT, XQueryParser.DDOT, XQueryParser.COLON, XQueryParser.COLON_EQ, XQueryParser.SEMICOLON, XQueryParser.SLASH, XQueryParser.DSLASH, XQueryParser.BACKSLASH, XQueryParser.VBAR, XQueryParser.RANGLE, XQueryParser.QUESTION, XQueryParser.AT, XQueryParser.DOLLAR, XQueryParser.MOD, XQueryParser.BANG, XQueryParser.HASH, XQueryParser.CARAT, XQueryParser.ARROW, XQueryParser.GRAVE, XQueryParser.TILDE, XQueryParser.KW_ALLOWING, XQueryParser.KW_ANCESTOR, XQueryParser.KW_ANCESTOR_OR_SELF, XQueryParser.KW_AND, XQueryParser.KW_ARRAY, XQueryParser.KW_AS, XQueryParser.KW_ASCENDING, XQueryParser.KW_AT, XQueryParser.KW_ATTRIBUTE, XQueryParser.KW_BASE_URI, XQueryParser.KW_BOUNDARY_SPACE, XQueryParser.KW_BINARY, XQueryParser.KW_BY, XQueryParser.KW_CASE, XQueryParser.KW_CAST, XQueryParser.KW_CASTABLE, XQueryParser.KW_CATCH, XQueryParser.KW_CHILD, XQueryParser.KW_COLLATION, XQueryParser.KW_COMMENT, XQueryParser.KW_CONSTRUCTION, XQueryParser.KW_CONTEXT, XQueryParser.KW_COPY_NS, XQueryParser.KW_COUNT, XQueryParser.KW_DECLARE, XQueryParser.KW_DEFAULT, XQueryParser.KW_DESCENDANT, XQueryParser.KW_DESCENDANT_OR_SELF, XQueryParser.KW_DESCENDING, XQueryParser.KW_DECIMAL_FORMAT, XQueryParser.KW_DIV, XQueryParser.KW_DOCUMENT, XQueryParser.KW_DOCUMENT_NODE, XQueryParser.KW_ELEMENT, XQueryParser.KW_ELSE, XQueryParser.KW_EMPTY, XQueryParser.KW_EMPTY_SEQUENCE, XQueryParser.KW_ENCODING, XQueryParser.KW_END, XQueryParser.KW_EQ, XQueryParser.KW_EVERY, XQueryParser.KW_EXCEPT, XQueryParser.KW_EXTERNAL, XQueryParser.KW_FOLLOWING, XQueryParser.KW_FOLLOWING_SIBLING, XQueryParser.KW_FOR, XQueryParser.KW_FUNCTION, XQueryParser.KW_GE, XQueryParser.KW_GREATEST, XQueryParser.KW_GROUP, XQueryParser.KW_GT, XQueryParser.KW_IDIV, XQueryParser.KW_IF, XQueryParser.KW_IMPORT, XQueryParser.KW_IN, XQueryParser.KW_INHERIT, XQueryParser.KW_INSTANCE, XQueryParser.KW_INTERSECT, XQueryParser.KW_IS, XQueryParser.KW_ITEM, XQueryParser.KW_LAX, XQueryParser.KW_LE, XQueryParser.KW_LEAST, XQueryParser.KW_LET, XQueryParser.KW_LT, XQueryParser.KW_MAP, XQueryParser.KW_MOD, XQueryParser.KW_MODULE, XQueryParser.KW_NAMESPACE, XQueryParser.KW_NE, XQueryParser.KW_NEXT, XQueryParser.KW_NAMESPACE_NODE, XQueryParser.KW_NO_INHERIT, XQueryParser.KW_NO_PRESERVE, XQueryParser.KW_NODE, XQueryParser.KW_OF, XQueryParser.KW_ONLY, XQueryParser.KW_OPTION, XQueryParser.KW_OR, XQueryParser.KW_ORDER, XQueryParser.KW_ORDERED, XQueryParser.KW_ORDERING, XQueryParser.KW_PARENT, XQueryParser.KW_PRECEDING, XQueryParser.KW_PRECEDING_SIBLING, XQueryParser.KW_PRESERVE, XQueryParser.KW_PREVIOUS, XQueryParser.KW_PI, XQueryParser.KW_RETURN, XQueryParser.KW_SATISFIES, XQueryParser.KW_SCHEMA, XQueryParser.KW_SCHEMA_ATTR, XQueryParser.KW_SCHEMA_ELEM, XQueryParser.KW_SELF, XQueryParser.KW_SLIDING, XQueryParser.KW_SOME, XQueryParser.KW_STABLE, XQueryParser.KW_START, XQueryParser.KW_STRICT, XQueryParser.KW_STRIP, XQueryParser.KW_SWITCH, XQueryParser.KW_TEXT, XQueryParser.KW_THEN, XQueryParser.KW_TO, XQueryParser.KW_TREAT, XQueryParser.KW_TRY, XQueryParser.KW_TUMBLING, XQueryParser.KW_TYPE, XQueryParser.KW_TYPESWITCH, XQueryParser.KW_UNION, XQueryParser.KW_UNORDERED, XQueryParser.KW_UPDATE, XQueryParser.KW_VALIDATE, XQueryParser.KW_VARIABLE, XQueryParser.KW_VERSION, XQueryParser.KW_WHEN, XQueryParser.KW_WHERE, XQueryParser.KW_WINDOW, XQueryParser.KW_XQUERY, XQueryParser.KW_ARRAY_NODE, XQueryParser.KW_BOOLEAN_NODE, XQueryParser.KW_NULL_NODE, XQueryParser.KW_NUMBER_NODE, XQueryParser.KW_OBJECT_NODE, XQueryParser.KW_REPLACE, XQueryParser.KW_WITH, XQueryParser.KW_VALUE, XQueryParser.KW_INSERT, XQueryParser.KW_INTO, XQueryParser.KW_DELETE, XQueryParser.KW_RENAME, XQueryParser.URIQualifiedName, XQueryParser.FullQName, XQueryParser.NCNameWithLocalWildcard, XQueryParser.NCNameWithPrefixWildcard, XQueryParser.NCName, XQueryParser.XQDOC_COMMENT_START, XQueryParser.ContentChar]:
                    self.state = 2095
                    self.stringContentApos()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 2100
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2101
            self.match(XQueryParser.Apos)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringLiteralQuot(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralQuotContext,0)


        def stringLiteralApos(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralAposContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_stringLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteral" ):
                listener.enterStringLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteral" ):
                listener.exitStringLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteral" ):
                return visitor.visitStringLiteral(self)
            else:
                return visitor.visitChildren(self)




    def stringLiteral(self):

        localctx = XQueryParser.StringLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 472, self.RULE_stringLiteral)
        try:
            self.state = 2105
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [XQueryParser.Quot]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2103
                self.stringLiteralQuot()
                pass
            elif token in [XQueryParser.Apos]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2104
                self.stringLiteralApos()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContentQuotContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ContentChar(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ContentChar)
            else:
                return self.getToken(XQueryParser.ContentChar, i)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def DOUBLE_LBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_LBRACE, 0)

        def DOUBLE_RBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_RBRACE, 0)

        def noQuotesNoBracesNoAmpNoLAng(self):
            return self.getTypedRuleContext(XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext,0)


        def stringLiteralApos(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralAposContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_stringContentQuot

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringContentQuot" ):
                listener.enterStringContentQuot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringContentQuot" ):
                listener.exitStringContentQuot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringContentQuot" ):
                return visitor.visitStringContentQuot(self)
            else:
                return visitor.visitChildren(self)




    def stringContentQuot(self):

        localctx = XQueryParser.StringContentQuotContext(self, self._ctx, self.state)
        self.enterRule(localctx, 474, self.RULE_stringContentQuot)
        try:
            self.state = 2124
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,201,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2108 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 2107
                        self.match(XQueryParser.ContentChar)

                    else:
                        raise NoViableAltException(self)
                    self.state = 2110 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,198,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2112
                self.match(XQueryParser.LBRACE)
                self.state = 2114
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,199,self._ctx)
                if la_ == 1:
                    self.state = 2113
                    self.expr()


                self.state = 2117
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,200,self._ctx)
                if la_ == 1:
                    self.state = 2116
                    self.match(XQueryParser.RBRACE)


                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 2119
                self.match(XQueryParser.RBRACE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 2120
                self.match(XQueryParser.DOUBLE_LBRACE)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 2121
                self.match(XQueryParser.DOUBLE_RBRACE)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 2122
                self.noQuotesNoBracesNoAmpNoLAng()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 2123
                self.stringLiteralApos()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContentAposContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ContentChar(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ContentChar)
            else:
                return self.getToken(XQueryParser.ContentChar, i)

        def LBRACE(self):
            return self.getToken(XQueryParser.LBRACE, 0)

        def expr(self):
            return self.getTypedRuleContext(XQueryParser.ExprContext,0)


        def RBRACE(self):
            return self.getToken(XQueryParser.RBRACE, 0)

        def DOUBLE_LBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_LBRACE, 0)

        def DOUBLE_RBRACE(self):
            return self.getToken(XQueryParser.DOUBLE_RBRACE, 0)

        def noQuotesNoBracesNoAmpNoLAng(self):
            return self.getTypedRuleContext(XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext,0)


        def stringLiteralQuot(self):
            return self.getTypedRuleContext(XQueryParser.StringLiteralQuotContext,0)


        def getRuleIndex(self):
            return XQueryParser.RULE_stringContentApos

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringContentApos" ):
                listener.enterStringContentApos(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringContentApos" ):
                listener.exitStringContentApos(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringContentApos" ):
                return visitor.visitStringContentApos(self)
            else:
                return visitor.visitChildren(self)




    def stringContentApos(self):

        localctx = XQueryParser.StringContentAposContext(self, self._ctx, self.state)
        self.enterRule(localctx, 476, self.RULE_stringContentApos)
        try:
            self.state = 2143
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,205,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2127 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 2126
                        self.match(XQueryParser.ContentChar)

                    else:
                        raise NoViableAltException(self)
                    self.state = 2129 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,202,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2131
                self.match(XQueryParser.LBRACE)
                self.state = 2133
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,203,self._ctx)
                if la_ == 1:
                    self.state = 2132
                    self.expr()


                self.state = 2136
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,204,self._ctx)
                if la_ == 1:
                    self.state = 2135
                    self.match(XQueryParser.RBRACE)


                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 2138
                self.match(XQueryParser.RBRACE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 2139
                self.match(XQueryParser.DOUBLE_LBRACE)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 2140
                self.match(XQueryParser.DOUBLE_RBRACE)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 2141
                self.noQuotesNoBracesNoAmpNoLAng()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 2142
                self.stringLiteralQuot()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NoQuotesNoBracesNoAmpNoLAngContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def keyword(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XQueryParser.KeywordContext)
            else:
                return self.getTypedRuleContext(XQueryParser.KeywordContext,i)


        def IntegerLiteral(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.IntegerLiteral)
            else:
                return self.getToken(XQueryParser.IntegerLiteral, i)

        def DecimalLiteral(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DecimalLiteral)
            else:
                return self.getToken(XQueryParser.DecimalLiteral, i)

        def DoubleLiteral(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DoubleLiteral)
            else:
                return self.getToken(XQueryParser.DoubleLiteral, i)

        def PRAGMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PRAGMA)
            else:
                return self.getToken(XQueryParser.PRAGMA, i)

        def EQUAL(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.EQUAL)
            else:
                return self.getToken(XQueryParser.EQUAL, i)

        def HASH(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.HASH)
            else:
                return self.getToken(XQueryParser.HASH, i)

        def NOT_EQUAL(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.NOT_EQUAL)
            else:
                return self.getToken(XQueryParser.NOT_EQUAL, i)

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.LPAREN)
            else:
                return self.getToken(XQueryParser.LPAREN, i)

        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.RPAREN)
            else:
                return self.getToken(XQueryParser.RPAREN, i)

        def LBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.LBRACKET)
            else:
                return self.getToken(XQueryParser.LBRACKET, i)

        def RBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.RBRACKET)
            else:
                return self.getToken(XQueryParser.RBRACKET, i)

        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.STAR)
            else:
                return self.getToken(XQueryParser.STAR, i)

        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.PLUS)
            else:
                return self.getToken(XQueryParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.MINUS)
            else:
                return self.getToken(XQueryParser.MINUS, i)

        def TILDE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.TILDE)
            else:
                return self.getToken(XQueryParser.TILDE, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMA)
            else:
                return self.getToken(XQueryParser.COMMA, i)

        def ARROW(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ARROW)
            else:
                return self.getToken(XQueryParser.ARROW, i)

        def KW_NEXT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_NEXT)
            else:
                return self.getToken(XQueryParser.KW_NEXT, i)

        def KW_PREVIOUS(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.KW_PREVIOUS)
            else:
                return self.getToken(XQueryParser.KW_PREVIOUS, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.MOD)
            else:
                return self.getToken(XQueryParser.MOD, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DOT)
            else:
                return self.getToken(XQueryParser.DOT, i)

        def GRAVE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.GRAVE)
            else:
                return self.getToken(XQueryParser.GRAVE, i)

        def DDOT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DDOT)
            else:
                return self.getToken(XQueryParser.DDOT, i)

        def XQDOC_COMMENT_START(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.XQDOC_COMMENT_START)
            else:
                return self.getToken(XQueryParser.XQDOC_COMMENT_START, i)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COLON)
            else:
                return self.getToken(XQueryParser.COLON, i)

        def CARAT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.CARAT)
            else:
                return self.getToken(XQueryParser.CARAT, i)

        def COLON_EQ(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COLON_EQ)
            else:
                return self.getToken(XQueryParser.COLON_EQ, i)

        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.SEMICOLON)
            else:
                return self.getToken(XQueryParser.SEMICOLON, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.SLASH)
            else:
                return self.getToken(XQueryParser.SLASH, i)

        def DSLASH(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DSLASH)
            else:
                return self.getToken(XQueryParser.DSLASH, i)

        def BACKSLASH(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.BACKSLASH)
            else:
                return self.getToken(XQueryParser.BACKSLASH, i)

        def COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.COMMENT)
            else:
                return self.getToken(XQueryParser.COMMENT, i)

        def VBAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.VBAR)
            else:
                return self.getToken(XQueryParser.VBAR, i)

        def RANGLE(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.RANGLE)
            else:
                return self.getToken(XQueryParser.RANGLE, i)

        def QUESTION(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.QUESTION)
            else:
                return self.getToken(XQueryParser.QUESTION, i)

        def AT(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.AT)
            else:
                return self.getToken(XQueryParser.AT, i)

        def DOLLAR(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.DOLLAR)
            else:
                return self.getToken(XQueryParser.DOLLAR, i)

        def BANG(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.BANG)
            else:
                return self.getToken(XQueryParser.BANG, i)

        def FullQName(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.FullQName)
            else:
                return self.getToken(XQueryParser.FullQName, i)

        def URIQualifiedName(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.URIQualifiedName)
            else:
                return self.getToken(XQueryParser.URIQualifiedName, i)

        def NCNameWithLocalWildcard(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.NCNameWithLocalWildcard)
            else:
                return self.getToken(XQueryParser.NCNameWithLocalWildcard, i)

        def NCNameWithPrefixWildcard(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.NCNameWithPrefixWildcard)
            else:
                return self.getToken(XQueryParser.NCNameWithPrefixWildcard, i)

        def NCName(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.NCName)
            else:
                return self.getToken(XQueryParser.NCName, i)

        def ContentChar(self, i:int=None):
            if i is None:
                return self.getTokens(XQueryParser.ContentChar)
            else:
                return self.getToken(XQueryParser.ContentChar, i)

        def getRuleIndex(self):
            return XQueryParser.RULE_noQuotesNoBracesNoAmpNoLAng

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNoQuotesNoBracesNoAmpNoLAng" ):
                listener.enterNoQuotesNoBracesNoAmpNoLAng(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNoQuotesNoBracesNoAmpNoLAng" ):
                listener.exitNoQuotesNoBracesNoAmpNoLAng(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNoQuotesNoBracesNoAmpNoLAng" ):
                return visitor.visitNoQuotesNoBracesNoAmpNoLAng(self)
            else:
                return visitor.visitChildren(self)




    def noQuotesNoBracesNoAmpNoLAng(self):

        localctx = XQueryParser.NoQuotesNoBracesNoAmpNoLAngContext(self, self._ctx, self.state)
        self.enterRule(localctx, 478, self.RULE_noQuotesNoBracesNoAmpNoLAng)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2147 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 2147
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,206,self._ctx)
                    if la_ == 1:
                        self.state = 2145
                        self.keyword()
                        pass

                    elif la_ == 2:
                        self.state = 2146
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << XQueryParser.IntegerLiteral) | (1 << XQueryParser.DecimalLiteral) | (1 << XQueryParser.DoubleLiteral) | (1 << XQueryParser.COMMENT) | (1 << XQueryParser.PRAGMA) | (1 << XQueryParser.EQUAL) | (1 << XQueryParser.NOT_EQUAL) | (1 << XQueryParser.LPAREN) | (1 << XQueryParser.RPAREN) | (1 << XQueryParser.LBRACKET) | (1 << XQueryParser.RBRACKET) | (1 << XQueryParser.STAR) | (1 << XQueryParser.PLUS) | (1 << XQueryParser.MINUS) | (1 << XQueryParser.COMMA) | (1 << XQueryParser.DOT) | (1 << XQueryParser.DDOT) | (1 << XQueryParser.COLON) | (1 << XQueryParser.COLON_EQ) | (1 << XQueryParser.SEMICOLON) | (1 << XQueryParser.SLASH) | (1 << XQueryParser.DSLASH) | (1 << XQueryParser.BACKSLASH) | (1 << XQueryParser.VBAR) | (1 << XQueryParser.RANGLE) | (1 << XQueryParser.QUESTION) | (1 << XQueryParser.AT) | (1 << XQueryParser.DOLLAR) | (1 << XQueryParser.MOD) | (1 << XQueryParser.BANG) | (1 << XQueryParser.HASH) | (1 << XQueryParser.CARAT) | (1 << XQueryParser.ARROW) | (1 << XQueryParser.GRAVE) | (1 << XQueryParser.TILDE))) != 0) or ((((_la - 123)) & ~0x3f) == 0 and ((1 << (_la - 123)) & ((1 << (XQueryParser.KW_NEXT - 123)) | (1 << (XQueryParser.KW_PREVIOUS - 123)) | (1 << (XQueryParser.URIQualifiedName - 123)) | (1 << (XQueryParser.FullQName - 123)) | (1 << (XQueryParser.NCNameWithLocalWildcard - 123)))) != 0) or ((((_la - 187)) & ~0x3f) == 0 and ((1 << (_la - 187)) & ((1 << (XQueryParser.NCNameWithPrefixWildcard - 187)) | (1 << (XQueryParser.NCName - 187)) | (1 << (XQueryParser.XQDOC_COMMENT_START - 187)) | (1 << (XQueryParser.ContentChar - 187)))) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass



                else:
                    raise NoViableAltException(self)
                self.state = 2149 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,207,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





