function saveFig(name)
% saveFig  Save current figure to ./figures at 300 dpi PNG
    folder = "figures";
    if ~isfolder(folder), mkdir(folder); end
    exportgraphics(gcf, fullfile(folder,name), "Resolution",300);
end
