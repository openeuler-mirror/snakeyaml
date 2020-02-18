#Global macro or variable
%global vertag 70abb5efa4c0

#Basic Information
Name:           snakeyaml
Version:        1.17
Release:        8
Summary:        YAML parser and emitter for the Java programming language
License:        ASL 2.0
URL:            https://bitbucket.org/asomov/%{name}/
Source0:        https://bitbucket.org/asomov/snakeyaml/get/v%{version}.tar.bz2#/%{name}-%{version}.tar.bz2
BuildArch:      noarch

#Dependency
BuildRequires:  dos2unix maven-local
BuildRequires:  mvn(biz.source_code:base64coder) mvn(commons-codec:commons-codec)
BuildRequires:  mvn(joda-time:joda-time) mvn(org.apache.velocity:velocity)
BuildRequires:  mvn(junit:junit) mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)

%description
SnakeYAML is a YAML parser and emitter for the Java Virtual Machine.
YAML is a data serialization format designed for human readability
and interaction with scripting languages.

SnakeYAML features:
  * a complete YAML 1.1 parser. In particular,
    SnakeYAML can parse all examples from the specification.
  * Unicode support including UTF-8/UTF-16 input/output.
  * high-level API for serializing and deserializing native Java objects.
  * support for all types from the YAML types repository.
  * relatively sensible error messages.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains javadoc for %{name}.

#Build sections
%prep
%autosetup -n asomov-%{name}-%{vertag} -p1

%mvn_file : %{name}

dos2unix LICENSE.txt

%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :maven-changes-plugin
%pom_remove_plugin :maven-license-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-site-plugin

sed -i "/<artifactId>spring</s/spring/&-core/" pom.xml
rm -f src/test/java/examples/SpringTest.java

%pom_add_dep commons-codec:commons-codec
%pom_add_dep biz.source_code:base64coder

rm -rf target
rm src/test/java/org/yaml/snakeyaml/issues/issue67/NonAsciiCharsInClassNameTest.java
rm src/test/java/org/yaml/snakeyaml/issues/issue318/ContextClassLoaderTest.java
 
%pom_remove_dep org.springframework
rm -r src/test/java/org/yaml/snakeyaml/issues/issue9

%build
%mvn_build

%install
%mvn_install

#Files list
%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Tue Feb 11 2020 Jiangping Hu <hujp1985@foxmail.com> - 1.17-8
- Package init

