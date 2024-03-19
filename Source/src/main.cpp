#include "../headers/mainwindow.h"

#include <QApplication>
#include <QLocale>
#include <QTranslator>

#include <QLoggingCategory>
#include <QDebug>

int main(int argc, char *argv[])
{
    qputenv("QT_LOGGING_RULES", "qt.memory=true"); // Enable the memory tracking

    QLoggingCategory::setFilterRules(QStringLiteral("qt.memory=true")); // Enable the memory tracking

    QApplication a(argc, argv);

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "TODO_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            a.installTranslator(&translator);
            break;
        }
    }
    MainWindow w;

    w.show();
    return a.exec();
}
